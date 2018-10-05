import os
import unittest
from base64 import b64encode
from requests.auth import _basic_auth_str

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

    def testGetRevokeToken(self):
        usr = {
            'username': 'sathouel',
            'email': 'sathouel@tst.com',
            'password': 'test'
        }
        # register usr
        resp = self.client.post('/auth/register', json=usr)
        self.assertEqual(resp.status_code, 201)
        username, password = usr['username'], usr['password']
        user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.check_password('test'), True)

        # get token
        headers = {
            'Authorization': _basic_auth_str(username, password)
        }
        resp = self.client.post('auth/tokens', headers=headers)
        status_code, data_json = resp.status_code, resp.json
        self.assertEqual(status_code, 200)
        token = data_json.get('token')
        self.assertIsNotNone(token)

        # test_token_auth_required
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        resp = self.client.delete('/auth/tokens', headers=headers)
        self.assertEqual(resp.status_code, 204)



if __name__ == '__main__':
    unittest.main()
