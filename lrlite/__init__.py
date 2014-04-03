from pyramid.config import Configurator
from pprint import pformat
import requests
import multiprocessing
try:
    import uwsgi
except:
    pass
from couchdbkit import *
from couchdbkit.changes import ChangesStream, foreach
from pyramid.security import remember
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.security import Authenticated, Allow, Everyone, ALL_PERMISSIONS
from pyramid.authorization import ACLAuthorizationPolicy
from logging import getLogger
log = getLogger(__name__)
_UPDATE_VIEW = 'update_view'



def update_views(db_uri):
    resp = requests.get(db_uri + '/_all_docs', params={
        'startkey': '"_design/"',
        'endkey': '"_design0"'
    })
    data = resp.json()
    for design_doc in data['rows']:
        doc = requests.get(db_uri + '/' + design_doc['id']).json()
        for k in doc['views']:
            view_result = requests.get(
                db_uri + '/' + design_doc['id'] + '/_view/' + k, params={'stale': 'update_after', "limit": 1}).json()


def monitor_changes(db):
    previous_seq = 0
    count = 0
    while True:
        stream = ChangesStream(db, feed="continuous",
                               heartbeat=True, since=previous_seq)
        log.debug("pull from changes")
        for c in stream:
            previous_seq = c['seq']
            count += 1
            if count % 100 == 0:
                log.debug("updating views")
                try:
                    uwsgi.spool({"action": _UPDATE_VIEW, "uri": db.uri})
                except:
                    pass


def spooler(env):
    action = env.get('action')
    if action == _UPDATE_VIEW:
        update_views(env['uri'])
        return uwsgi.SPOOL_OK
    else:
        log.error("Unknow Task: {0}".format(pformat(env)))
        return uwsgi.SPOOL_OK
try:
    uwsgi.spooler = spooler
except:
    pass


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
    config.add_route("signin", '/signin')
    config.add_route("signout", '/signout')
    config.add_route("userkey", '/user/:username/key')
    config.include('lrlite.api', route_prefix="/v1")
    p = multiprocessing.Process(target=monitor_changes, args=(
        config.registry.db.get_or_create_db(settings['couchdb.db']), ))
    p.start()
    config.scan()
    return config.make_wsgi_app()
