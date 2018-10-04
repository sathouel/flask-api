import os
import unittest

from api import create_app, db
from api.config import TestConfig
from api.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_hello(self):
        resp = self.client.get('/auth/tst')
        print(resp)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
