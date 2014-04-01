from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import json
import base64
import requests
import gnupg
from pyramid.security import authenticated_userid
from .models import *
from logging import getLogger
from couchdbkit.exceptions import ResourceConflict
log = getLogger(__name__)
_SESSION = "session"

def _validate_param(param):
    return param is not None and len(param) > 0


@view_config(route_name='home', renderer='templates/mytemplate.pt', request_method="GET")
def home(req):
    if _SESSION in req.cookies:
        session_info = json.loads(base64.b64decode(req.cookies[_SESSION]))        
        user = get_user(req.users, session_info['user'], session_info['key'])
        rv = {'project': 'LR-Lite', "signed_in": True, }
        rv.update(user)
        rv['key_location'] = req.route_url("userkey", username=session_info['user'])
        return rv        
    else:
        return {'project': 'LR-Lite', "signed_in": False}


@view_config(route_name="signup", renderer="templates/signup.pt", request_method="GET")
def signup(req):
    return {"success": True}


@view_config(route_name='signup', renderer='templates/signup.pt', request_method="POST")
def create_user(req):
    username = req.POST.get('username', "").strip()
    password = req.POST.get('password', "").strip()
    repassword = req.POST.get('repassword', "").strip()
    if not _validate_param(username):
        return {'project': 'LR-Lite', "success": False, "error": "Username is required"}
    if not _validate_param(password) or not _validate_param(repassword):
        return {'project': 'LR-Lite', "success": False, "error": "Password is required"}
    if password != repassword:
        return {'project': 'LR-Lite', "success": False, "error": "Passwords do not match"}
    try:
        create_new_user(req.users, username, password)
        return {'project': 'LR-Lite', "success": True}
    except ResourceConflict:
        return {'project': 'LR-Lite', "success": False, "error": "Username already in use"}


@view_config(route_name="signin", renderer="templates/signin.pt", request_method="GET")
def signin_get(req):
    if _SESSION in req.cookies:
        raise HTTPFound(req.route_url("home"), headers=req.response.headers)
    else:
        return {'project': 'LR-Lite', "signed_in": False}


@view_config(route_name="signin", renderer="templates/signin.pt", request_method="POST")
def signin_post(req):    
    username = req.POST.get('username', "").strip()
    password = req.POST.get('password', "").strip()
    data = {"name": username, "password": password}    
    response = requests.post(req.db.server_uri + "/_session", data=data)
    if response.ok:
        user_cookie = response.headers['set-cookie']
        req.response.set_cookie(_SESSION, base64.b64encode(json.dumps({'key': user_cookie, "user": username})))
        raise HTTPFound(req.route_url("home"), headers=req.response.headers)
    else:
        return {'project': 'LR-Lite', "signed_in": False}


@view_config(route_name="userkey", renderer="string", request_method="GET")
def get_user_key(req):
    gpg = gnupg.GPG()
    username = req.matchdict['username']
    data = req.users['org.couchdb.user:' + username]
    return gpg.export_keys(data.get('keyid'))

@view_config(route_name="signout", renderer="string")
def signout(req):
    req.response.delete_cookie(_SESSION)
    raise HTTPFound(req.route_url("home"), headers=req.response.headers)