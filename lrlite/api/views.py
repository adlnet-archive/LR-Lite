
from pyramid.view import view_config
from lib.validation import *
from logging import getLogger
import json
logger = getLogger(__name__)

@view_config(route_name="api", renderer="json", request_method="PUT")
def add_envelope(req):
	data = json.loads(req.body)
	validators = [validate_schema, validate_signature]
	valid_result = reduce(lambda prev, v: prev and v(data), validators, True)
	return {"OK": valid_result}

@view_config(route_name="api", renderer="json", request_method="GET")
def retrieveList(req):
	return {"OK": True}

@view_config(route_name="document", renderer="json", request_method="GET")
def retriveEnvelope(req):
	return {"target": req.matchdict.get("doc_id")}

@view_config(route_name="document", renderer="json", request_method="POST")
def updateDocumetn(req):
	return {"target": req.matchdict.get("doc_id")}