import unittest
from couchdbkit import *
from pyramid import testing
from .views import *
from .models import *


class ModelTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.testConfig()

    def tearDown(self):
        testing.tearDown()

    def test_create_user(self):
        db = Database("http://admin:password@localhost:5984/_users")
        create_new_user(db, "user", "password")
