import os
import unittest

from api import create_app, db
from api.config import TestConfig
from api.models import User


class TestAuth(unittest.TestCase):
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

    def testRegisterUser(self):
        u1 = {
            'username': 'michel',
            'email': 'michel@tst.com',
            'password': 'tstpwd'
        }
        u2 = {
            'username': 'michel',
            'email': 'test@test.com',
            'password': 'tstpwd'
        }
        u3 = {
            'username': 'jean',
            'email': 'michel@tst.com',
            'password': 'tstpwd'
        }
        error_message1 = 'please use a different username'
        error_message2 = 'please use a different email'
        error_message3 = 'no data provided'

        # Working case
        resp = self.client.post('/auth/register', json=u1)
        self.assertEqual(resp.status_code, 201)
        user = User.query.filter_by(username='michel').first()
        self.assertEqual(user.username, u1['username'])
        self.assertEqual(user.email, u1['email'])
        users = User.query.all()
        self.assertEqual(len(users), 1)

        # Same username
        resp2 = self.client.post('/auth/register', json=u1)
        resp3 = self.client.post('/auth/register', json=u2)
        resp4 = self.client.post('/auth/register', json=u3)
        resp5 = self.client.post('/auth/register', json={})

        self.assertEqual(resp2.status_code, 400)
        self.assertEqual(resp2.json['message'], error_message1)

        self.assertEqual(resp3.status_code, 400)
        self.assertEqual(resp3.json['message'], error_message1)

        self.assertEqual(resp4.status_code, 400)
        self.assertEqual(resp4.json['message'], error_message2)

        self.assertEqual(resp5.status_code, 400)
        self.assertEqual(resp5.json['message'], error_message3)

        users = User.query.all()
        self.assertEqual(len(users), 1)

    def testLoginUser(self):
        usr = {
            'username': 'sathouel',
            'email': 'sathouel@tst.com',
            'password': 'test'
        }
        resp = self.client.post('/auth/register', json=usr)
        self.assertEqual(resp.status_code, 201)




if __name__ == '__main__':
    unittest.main()
