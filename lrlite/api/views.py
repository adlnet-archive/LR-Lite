from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from pyramid.response import Response
from lib.validation import *
from logging import getLogger
import json
import uuid
import calendar
from datetime import datetime
import requests
import ijson
import iso8601
import pdb
log = getLogger(__name__)


def _populate_node_values(envelope, req):
    if 'doc_ID' not in envelope:
        doc_id = uuid.uuid4().hex
        envelope['doc_ID'] = doc_id
    current_time = datetime.utcnow().isoformat() + 'Z'
    for k in ['node_timestamp', 'create_timestamp', 'update_timestamp']:
        envelope[k] = current_time
    envelope['publishing_node'] = req.node_id

def _parse_retrieve_params(req):    
    params = {"limit": 10, "stale": "update_after"}
    include_docs = req.GET.get("include_docs", False)
    if not isinstance(include_docs, bool):
        try:
            include_docs = json.loads(include_docs)
            params['include_docs'] = include_docs
        except Exception as ex:
            log.exception(ex)
            raise HTTPBadRequest("Invalid JSON for include_docs")
    try:
        time = iso8601.parse_date(req.GET.get("from", datetime.min.isoformat()))
        params['startkey'] = calendar.timegm(time.utctimetuple())
    except Exception as ex:
        log.exception(ex)
        raise HTTPBadRequest("Invalid from time, must be ISO 8601 format")
    try:
        time = iso8601.parse_date(req.GET.get("until", datetime.utcnow().isoformat()))
        params['endkey'] = calendar.timegm(time.utctimetuple())
    except Exception as ex:
        log.exception(ex)
        raise HTTPBadRequest("Invalid until time, must be ISO 8601 format")            
    if params['endkey'] < params['startkey']:
        raise HTTPBadRequest("From date cannot come after until date")            
    return params

@view_config(route_name="api", renderer="json", request_method="PUT")
def add_envelope(req):
    data = json.loads(req.body)
    _populate_node_values(data, req)
    if data['doc_ID'] in req.db:
        return {"OK": False, "msg": "doc_ID is taken"}
    result = validate_schema(data)
    if not result.success:
        return {"OK": False, "msg": result.message}
    result = validate_signature(data)
    if not result:
        return {"OK": False, "msg": "Invalid Signature"}
    req.db[data['doc_ID']] = data
    return {"OK": True, "doc_ID": data['doc_ID']}
        


@view_config(route_name="api", renderer="json", request_method="GET")
def retrieve_list(req):
    params = _parse_retrieve_params(req)
    def stream_results():        
        resp = requests.get(req.db.uri + "/_design/lr/_view/by-timestamp", stream=True, params=params)
        r = Response()
        item_selector = "rows.item.id"
        if params.get("include_docs"):
            item_selector = "rows.item.doc"
        items = ijson.items(resp.raw, item_selector)    
        first = True
        yield '['
        for x in items:
            if not first:
                yield ','
            first = False
            yield json.dumps(x)
        yield ']'        
    headers = {
        'Content-Type': 'application/json',
    }
    r = Response(headers=headers)
    r.app_iter = stream_results()
    return r


@view_config(route_name="document", renderer="json", request_method="GET")
def retriveEnvelope(req):
    try:
        return req.db[req.matchdict.get("doc_id")]
    except:
        raise HTTPNotFound()


@view_config(route_name="document", renderer="json", request_method="POST")
def updateDocumetn(req):
    return {"target": req.matchdict.get("doc_id")}
