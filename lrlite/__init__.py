from pyramid.config import Configurator
from couchdbkit import *
from pyramid.security import remember
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.security import Authenticated, Allow, Everyone, ALL_PERMISSIONS
from pyramid.authorization import ACLAuthorizationPolicy


class Root(object):

    """Simplest possible resource tree to map groups to permissions.
    """
    __acl__ = [
        (Allow, 'user', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


def auth_check(user, password, req):
    import requests
    data = {"name": user, "password": password}
    response = requests.post(req.db.server_uri + "/_session", data=data)
    data = response.json()
    roles = []
    roles.extend(data.get("roles", []))
    req.auth_cookie = response.headers['set-cookie']
    req.username = username
    return roles


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    authn_policy = BasicAuthAuthenticationPolicy(check=auth_check)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_authentication_policy(authn_policy)
    config.registry.db = Server(uri=settings['couchdb.uri'])

    def add_users(request):
        return config.registry.db.get_db("_users")

    def add_couchdb(request):
        db = config.registry.db.get_or_create_db(settings['couchdb.db'])
        return db

    def get_node_id(req):
        return settings['node.id']
    config.add_request_method(add_couchdb, 
                              'db', 
                              reify=True, 
                              property=True)
    config.add_request_method(add_users, 
                              "users", 
                              reify=True, 
                              property=True)
    config.add_request_method(get_node_id,
                              'node_id',
                              reify=True,
                              property=True)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route("signup", '/signup')
    config.add_route("userkey", '/user/:username/key')
    config.include('lrlite.api', route_prefix="/v1")
    config.scan()
    return config.make_wsgi_app()
