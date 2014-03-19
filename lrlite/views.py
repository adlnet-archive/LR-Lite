from pyramid.view import view_config
from .models import *
from logging import getLogger
from couchdbkit.exceptions import ResourceConflict
log = getLogger(__name__)

def _validate_param(param):
    return param is not None and len(param) > 0

@view_config(route_name='home', renderer='templates/mytemplate.pt', request_method="GET")
def home(request):
    return {'project': 'LR-Lite', "success": True, "error": "test"}


@view_config(route_name="signup", renderer="templates/signup.pt", request_method="GET")
def signup(req):
    return {"success": True}

@view_config(route_name='signup', renderer='templates/signup.pt', request_method="POST")
def create_user(req):
    username = req.POST.get('username')
    password = req.POST.get('password')
    repassword = req.POST.get('repassword')
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
