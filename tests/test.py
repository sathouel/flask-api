import os
import unittest

from api import app, db
from api.cofing import TestConfig
from api.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
