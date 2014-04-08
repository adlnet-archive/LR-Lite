import unittest
from .views import retrieve_list, delete_document, update_document
from pyramid.httpexceptions import HTTPBadRequest
import json
from couchdbkit import *
from pyramid import testing
from pprint import pformat
import iso8601


class ViewTests(unittest.TestCase):

    def add_couchdb(self, request):
        s = Server(uri="http://localhost:5984")
        db = s.get_or_create_db("resource_data")
        return db


    def setUp(self):
        config = testing.setUp()
        self.config = config
        self.config.add_route('userkey', '/user/:username/key')

    def tearDown(self):
        testing.tearDown()

    def _prepare_request(self, params):
        request = testing.DummyRequest()
        request.db = self.add_couchdb(request)
        s = Server(uri="http://admin:password@localhost:5984")
        request.users = s.get_db("_users")
        request.username = "wegrata3"
        request.node_id = "abc123"
        request.GET['include_docs'] = json.dumps(True)
        request.GET.update(params)
        return request

    def _list_test_generic(self, params, comparer):
        request = self._prepare_request(params)
        data = retrieve_list(request)        
        for envelope in data.json.get('response', []):            
            date = iso8601.parse_date(envelope.get("node_timestamp"))
            self.assertTrue(comparer(date))

    def test_get_list_from(self):
        params = {"from": "2012-10-26T15:14:02.972834Z"}
        from_date = iso8601.parse_date(params["from"])
        self._list_test_generic(params, lambda date: date >= from_date)

    def test_get_list_until(self):
        params = {"until": "2012-10-26T15:14:02.972834Z"}
        until_date = iso8601.parse_date(params["until"])
        self._list_test_generic(params, lambda date: date <= until_date)

    def test_get_list_from_until(self):
        params = {"until": "2012-11-26T15:14:02.972834Z",
                  "from": "2012-10-26T15:14:02.972834Z"}
        until_date = iso8601.parse_date(params["until"])
        from_date = iso8601.parse_date(params["from"])
        self._list_test_generic(
            params, lambda date: date <= until_date and date >= from_date)

    def test_get_list_until_from(self):
        params = {"from": "2012-11-26T15:14:02.972834Z",
                  "until": "2012-10-26T15:14:02.972834Z"}
        until_date = iso8601.parse_date(params["until"])
        from_date = iso8601.parse_date(params["from"])
        request = self._prepare_request(params)
        self.assertRaises(HTTPBadRequest, retrieve_list, request)

    def test_get_list_bad_from(self):
        params = {"from": "2012-11-"}
        request = self._prepare_request(params)
        self.assertRaises(HTTPBadRequest, retrieve_list, request)

    def test_get_list_bad_until(self):
        params = {"until": "2012-11-"}
        request = self._prepare_request(params)
        self.assertRaises(HTTPBadRequest, retrieve_list, request)

    def test_get_list_bad_include_docs(self):
        params = {"include_docs": "2012-11-"}
        request = self._prepare_request(params)
        self.assertRaises(HTTPBadRequest, retrieve_list, request)

    def test_add_envelope_lrmi(self):
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "",
            "digital_signature":            {
                "key_location": ["http://lrnode.inbloom.org/pubkey"],
                "key_owner": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "signing_method": "LR-PGP.1.0",
                "signature": "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nf01a16e10c15da435049150a1f8fe2b327b75055f0435412ad704f20c263336e\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (GNU/Linux)\n\niQEcBAEBAgAGBQJTAxNjAAoJEGNQ+N81sWR7TckIAKlaqlv0JPQxUOUxG4Ra3pXz\nl5nTxCzNAczOo/M3oODWERNvZbVaEsm7DtGlb41yHG6lTNm0ue3MMC2C0cfLCMjy\nLtYbi81t9GZG8qFpDEGpNsf+EUG7a25K8OE8NNwis1S66BL4Gb8fgEhUEfmlHNK2\npgaYcVSg15Yg6wCRb6C/at6U6z0ab1pVQ6lltet50RPsftJ3WabDEoHCem5255jl\nn4yHY7jmEP3Vkx7EvuHwa1MuBzTtB8q/GLRqY2+KrwKdaS8t4Igj/xgwxfUxGrKm\nGKEZc8t4N6CJ3KHwUPgaeSnGcgxLOsdktEunnbtGvanBszYWlo36T1WyDaKGWsI=\n=/tzy\n-----END PGP SIGNATURE-----\n"
            },
            "resource_data": {
                "items": [
                    {
                        "type": ["http://schema.org/CreativeWork"],
                        "id": "a4e87e49-b549-4499-ada5-9ec700226c2d",
                        "properties": {
                            "timeRequired": ["P0Y0M0W0DT0H0M0S"],
                            "inLanguage": ["es-ES"],
                            "educationalAlignment": [],
                            "name": ["Recurso 2"]
                        }
                    }
                ]
            },
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": [
                "schema.org",
                "LRMI",
                "application/microdata+json"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)
        assert info['OK']

    def test_add_envelope_str(self):
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)    
        assert info['OK'], pformat(info)

    def test_add_envelope_auto_sign(self):
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "http://test",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)    
        assert info['OK'], pformat(info)
        doc = request.db[info["doc_ID"]]
        assert "digital_signature" in doc

    def test_add_envelope_linked_fail(self):
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.node_id = "abc123"
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "linked",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)    
        assert not info['OK']


    def test_add_envelope_inline_fail(self):
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)    
        assert not info['OK'], pformat(info)

    def test_delete(self):
        import base64
        import gnupg
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'wegrata3', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "http://test",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)            
        assert info["OK"]
        request = testing.DummyRequest()        
        request.matchdict['doc_id'] = info['doc_ID']
        request.db = self.add_couchdb(request)
        s = Server(uri="http://admin:password@localhost:5984")
        request.users = s.get_db("_users")
        request.username = "wegrata3"
        result = delete_document(request)        
        assert result["OK"]
        assert request.db[info['doc_ID']].get('doc_type') == "tombstone"

    def test_update(self):
        import base64
        import gnupg
        from .views import add_envelope
        from requests import post
        request = self._prepare_request({})
        resp = post("http://localhost:5984/_session", data={"name": 'wegrata3', "password": 'password'})        
        request.auth_cookie = resp.headers['set-cookie']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "http://test",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })
        info = add_envelope(request)            
        assert info["OK"]
        request = testing.DummyRequest()        
        request.matchdict['doc_id'] = info['doc_ID']
        request.body = json.dumps({
            "doc_type": "resource_data",
            "resource_locator": "http://test123",
            "resource_data": "test",
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["plain text"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        })        
        request.db = self.add_couchdb(request)
        s = Server(uri="http://admin:password@localhost:5984")
        request.users = s.get_db("_users")
        request.username = "wegrata3"
        request.node_id = "abc123"
        request.auth_cookie = resp.headers['set-cookie']
        result = update_document(request)        
        assert result["OK"]
        print(result)
        assert request.db[info['doc_ID']].get('doc_type') == "tombstone"        
        assert result['doc_ID'] in request.db
