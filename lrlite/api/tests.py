import unittest
from .views import retrieve_list
from pyramid.httpexceptions import HTTPBadRequest
import json
from couchdbkit import *
from pyramid import testing
from pprint import pprint
import iso8601


class ViewTests(unittest.TestCase):

    def add_couchdb(self, request):
        s = Server(uri="http://admin:password@localhost:5984")
        db = s.get_or_create_db("resource_data")
        return db

    def setUp(self):
        config = testing.setUp()
        self.config = config

    def tearDown(self):
        testing.tearDown()

    def _prepare_request(self, params):
        request = testing.DummyRequest()
        request.db = self.add_couchdb(request)
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

    def test_add_envelope(self):
        from .views import add_envelope
        from requests import post
        resp = post("http://localhost:5984/_session", data={"name": 'user', "password": 'password'})        
        request = testing.DummyRequest()        
        request.db = self.add_couchdb(request)
        request.auth_cookie = resp.headers['set-cookie']
        request.node_id = "abc123"
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
