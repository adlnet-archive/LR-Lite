import unittest
from couchdbkit import *
from pyramid import testing
from .views import *
from .models import *
import uuid



class ModelTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.testConfig()

    def tearDown(self):
        testing.tearDown()

    def test_create_user(self):
    	username = uuid.uuid4().hex
        db = Database("http://admin:password@localhost:5984/_users")
        create_new_user(db, username, "password")
