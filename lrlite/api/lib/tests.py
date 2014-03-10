import unittest
from pyramid import testing
from lrlite.api.lib.validation import *


class ValidationTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.testConfig()

    def tearDown(self):
        testing.tearDown()
    

    def test_schema_validation_valid(self):
        envelope = {
            "doc_type": "resource_data",
            "resource_locator": "",
            "doc_ID": "123",
            "publishing_node": "abc",
            "update_timestamp": "2014-01-01T00:00:00Z",
            "create_timestamp": "2014-01-01T00:00:00Z",
            "node_timestamp": "2014-01-01T00:00:00Z",
            "digital_signature":            {
                "key_location": ["http://lrnode.inbloom.org/pubkey"],
                "key_owner": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "signing_method": "LR-PGP.1.0",
                "signature": "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nf01a16e10c15da435049150a1f8fe2b327b75055f0435412ad704f20c263336e\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (GNU/Linux)\n\niQEcBAEBAgAGBQJTAxNjAAoJEGNQ+N81sWR7TckIAKlaqlv0JPQxUOUxG4Ra3pXz\nl5nTxCzNAczOo/M3oODWERNvZbVaEsm7DtGlb41yHG6lTNm0ue3MMC2C0cfLCMjy\nLtYbi81t9GZG8qFpDEGpNsf+EUG7a25K8OE8NNwis1S66BL4Gb8fgEhUEfmlHNK2\npgaYcVSg15Yg6wCRb6C/at6U6z0ab1pVQ6lltet50RPsftJ3WabDEoHCem5255jl\nn4yHY7jmEP3Vkx7EvuHwa1MuBzTtB8q/GLRqY2+KrwKdaS8t4Igj/xgwxfUxGrKm\nGKEZc8t4N6CJ3KHwUPgaeSnGcgxLOsdktEunnbtGvanBszYWlo36T1WyDaKGWsI=\n=/tzy\n-----END PGP SIGNATURE-----\n"
            },
            "resource_data": {
                "items": [{
                    "type": ["http://schema.org/CreativeWork"],
                    "id": "a4e87e49-b549-4499-ada5-9ec700226c2d",
                    "properties": {
                        "timeRequired": ["P0Y0M0W0DT0H0M0S"],
                        "inLanguage": ["es-ES"],
                        "educationalAlignment": [],
                        "name": ["Recurso 2"]
                    }
                }]
            },
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["schema.org", "LRMI", "application/microdata+json"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        }
        assert validate_schema(envelope).success

    def test_schema_validation_invalid(self):
        envelope = {
            "doc_type": "resource_data",
            "resource_locator": "",
            "doc_ID": "123",
            "publishing_node": "abc",
            "update_timestamp": "2014-01-01T00:00:00Z",
            "create_timestamp": "2014-01-01T00:00:00Z",
            "node_timestamp": "2014-01-01T00:00:00Z",
            "digital_signature":            {
                "key_location": ["http://lrnode.inbloom.org/pubkey"],
                "key_owner": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "signing_method": "LR-PGP.1.0",
                "signature": "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nf01a16e10c15da435049150a1f8fe2b327b75055f0435412ad704f20c263336e\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (GNU/Linux)\n\niQEcBAEBAgAGBQJTAxNjAAoJEGNQ+N81sWR7TckIAKlaqlv0JPQxUOUxG4Ra3pXz\nl5nTxCzNAczOo/M3oODWERNvZbVaEsm7DtGlb41yHG6lTNm0ue3MMC2C0cfLCMjy\nLtYbi81t9GZG8qFpDEGpNsf+EUG7a25K8OE8NNwis1S66BL4Gb8fgEhUEfmlHNK2\npgaYcVSg15Yg6wCRb6C/at6U6z0ab1pVQ6lltet50RPsftJ3WabDEoHCem5255jl\nn4yHY7jmEP3Vkx7EvuHwa1MuBzTtB8q/GLRqY2+KrwKdaS8t4Igj/xgwxfUxGrKm\nGKEZc8t4N6CJ3KHwUPgaeSnGcgxLOsdktEunnbtGvanBszYWlo36T1WyDaKGWsI=\n=/tzy\n-----END PGP SIGNATURE-----\n"
            },
            "resource_data": {
                "items": [{
                    "type": ["http://schema.org/CreativeWork"],
                    "id": "a4e87e49-b549-4499-ada5-9ec700226c2d",
                    "properties": {
                        "timeRequired": ["P0Y0M0W0DT0H0M0S"],
                        "inLanguage": ["es-ES"],
                        "educationalAlignment": [],
                        "name": ["Recurso 2"]
                    }
                }]
            },
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["schema.org", "LRMI", "application/microdata+json"],
            "doc_version": "0.90.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        }
        assert not validate_schema(envelope).success and len(validate_schema(envelope).message)

    def test_signature_validation(self):
        envelope = {
            "doc_type": "resource_data",
            "resource_locator": "",
            "digital_signature":            {
                "key_location": ["http://lrnode.inbloom.org/pubkey"],
                "key_owner": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "signing_method": "LR-PGP.1.0",
                "signature": "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nf01a16e10c15da435049150a1f8fe2b327b75055f0435412ad704f20c263336e\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (GNU/Linux)\n\niQEcBAEBAgAGBQJTAxNjAAoJEGNQ+N81sWR7TckIAKlaqlv0JPQxUOUxG4Ra3pXz\nl5nTxCzNAczOo/M3oODWERNvZbVaEsm7DtGlb41yHG6lTNm0ue3MMC2C0cfLCMjy\nLtYbi81t9GZG8qFpDEGpNsf+EUG7a25K8OE8NNwis1S66BL4Gb8fgEhUEfmlHNK2\npgaYcVSg15Yg6wCRb6C/at6U6z0ab1pVQ6lltet50RPsftJ3WabDEoHCem5255jl\nn4yHY7jmEP3Vkx7EvuHwa1MuBzTtB8q/GLRqY2+KrwKdaS8t4Igj/xgwxfUxGrKm\nGKEZc8t4N6CJ3KHwUPgaeSnGcgxLOsdktEunnbtGvanBszYWlo36T1WyDaKGWsI=\n=/tzy\n-----END PGP SIGNATURE-----\n"
            },
            "resource_data": {
                "items": [{
                    "type": ["http://schema.org/CreativeWork"],
                    "id": "a4e87e49-b549-4499-ada5-9ec700226c2d",
                    "properties": {
                        "timeRequired": ["P0Y0M0W0DT0H0M0S"],
                        "inLanguage": ["es-ES"],
                        "educationalAlignment": [],
                        "name": ["Recurso 2"]
                    }
                }]
            },
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["schema.org", "LRMI", "application/microdata+json"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        }
        assert validate_signature(envelope).success

    def test_signature_validation_valid_sig_does_not_match(self):
        envelope = {
            "doc_type": "resource_data",
            "resource_locator": "",
            "digital_signature":            {
                "key_location": ["http://lrnode.inbloom.org/pubkey"],
                "key_owner": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "signing_method": "LR-PGP.1.0",
                "signature": "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nf01a16e10c15da435049150a1f8fe2b327b75055f0435412ad704f20c263336e\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (GNU/Linux)\n\niQEcBAEBAgAGBQJTAxNjAAoJEGNQ+N81sWR7TckIAKlaqlv0JPQxUOUxG4Ra3pXz\nl5nTxCzNAczOo/M3oODWERNvZbVaEsm7DtGlb41yHG6lTNm0ue3MMC2C0cfLCMjy\nLtYbi81t9GZG8qFpDEGpNsf+EUG7a25K8OE8NNwis1S66BL4Gb8fgEhUEfmlHNK2\npgaYcVSg15Yg6wCRb6C/at6U6z0ab1pVQ6lltet50RPsftJ3WabDEoHCem5255jl\nn4yHY7jmEP3Vkx7EvuHwa1MuBzTtB8q/GLRqY2+KrwKdaS8t4Igj/xgwxfUxGrKm\nGKEZc8t4N6CJ3KHwUPgaeSnGcgxLOsdktEunnbtGvanBszYWlo36T1WyDaKGWsI=\n=/tzy\n-----END PGP SIGNATURE-----\n"
            },
            "resource_data": {
                "items": [{
                    "type": ["http://schema.org/CreativeWork"],
                    "id": "a4e87e49-b549-4499-ada5-9ec700226c2d",
                    "properties": {
                        "timeRequired": ["P0Y0M0W0DT0H0M0S"],
                        "inLanguage": ["es-ES", "es-US"],
                        "educationalAlignment": [],
                        "name": ["Recurso 2"]
                    }
                }]
            },
            "keys": [],
            "TOS": {
                "submission_TOS": "http://www.learningregistry.org/information-assurances/open-information-assurances-1-0"
            },
            "resource_data_type": "metadata",
            "payload_schema_locator": "http://www.w3.org/TR/2012/WD-microdata-20121025/#converting-html-to-other-formats",
            "payload_placement": "inline",
            "payload_schema": ["schema.org", "LRMI", "application/microdata+json"],
            "doc_version": "0.23.0",
            "active": True,
            "identity": {
                "submitter": "inBloom Tagger Application <tagger@inbloom.org>",
                "signer": "Learning Registry SLC Node <lrnode@inbloom.org>",
                "submitter_type": "user",
                "curator": "5a4bfe96-1724-4565-9db1-35b3796e3ce1:jordi.juarez@udl.cat@null"
            }
        }
        assert validate_signature(envelope).success == False
