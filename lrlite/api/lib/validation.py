from LRSignature.verify.Verify import Verify_0_21, Verify_0_51, Verify_0_23
from pprint import pprint
from copy import deepcopy
from collections import namedtuple
from jsonschema import validate, Draft3Validator, ValidationError
import LRSignature.util as util
from .schema.validate import LRDraft3Validator
ValidationResult = namedtuple("ValidationResult", ["success", "message"])
gpg_location = "/usr/bin/gpg"
schema_ref = "file:lrlite/api/lib/schema/any/resource_data.json"
schema = {"$ref": schema_ref}
_ID = "_id"
_REV = "_rev"
_DOC_ID = "doc_ID"


def _get_verifier_for_version(version):
    if version == "0.21.0":
        return Verify_0_21(gpgbin=gpg_location)
    elif version == "0.23.0":
        return Verify_0_23(gpgbin=gpg_location)
    elif version == "0.51.0":
        return Verify_0_51(gpgbin=gpg_location)


def _import_keys(key_locations):
    num_imported = 0
    for loc in key_locations:
        raw_keys = util.fetchkeys(loc)
        for raw_key in raw_keys:
            num_imported += util.storekey(raw_key,
                                          gpgbin=gpg_location)
        if num_imported > 0:
            return


def validate_schema(envelope):
    model_ref = deepcopy(envelope)
    for k in [_ID, _REV]:
        if k in model_ref:
            del model_ref[k]
    try:
        validate(model_ref, schema, cls=LRDraft3Validator)
    except ValidationError as ve:
        msgs = []
        for err in LRDraft3Validator(schema).iter_errors(model_ref):
            msgs.append(err.message)
        return ValidationResult(success=False, message=msgs)
    return ValidationResult(success=True, message=[])


def validate_signature(envelope):
    _import_keys(envelope.get('digital_signature', {}).get('key_location', []))
    verifier = _get_verifier_for_version(envelope.get("doc_version"))
    v = verifier.verify(envelope)
    return ValidationResult(success=v, message=[])
