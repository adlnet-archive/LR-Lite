from pyramid.config import Configurator
from couchdbkit import *

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.registry.db = Server(uri=settings['couchdb.uri'])
    def add_couchdb(request):
        db = config.registry.db.get_or_create_db(settings['couchdb.db'])
        return db
    def get_node_id(req):
        return "abc123"
    config.add_request_method(add_couchdb, 'db', reify=True, property=True)    
    config.add_request_method(get_node_id, 'node_id', reify=True, property=True)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.include('lrlite.api', route_prefix="/v1")
    config.scan()
    return config.make_wsgi_app()
