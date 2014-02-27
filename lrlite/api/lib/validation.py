from LRSignature.verify.Verify import Verify_0_21, Verify_0_51, Verify_0_23
import LRSignature.util as util 
gpg_location = "/usr/bin/gpg"

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
    return True


def validate_signature(envelope):
    _import_keys(envelope.get('digital_signature', {}).get('key_location', []))
    verifier = _get_verifier_for_version(envelope.get("doc_version"))
    v = verifier.verify(envelope)
    return v
