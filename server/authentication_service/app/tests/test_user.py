import json
from unittest import TestCase

from flask_jwt_simple import create_jwt

from app import create_app, db as test_db
from app.config import TestConfig
from app.models import User, Verification

test_app = create_app(TestConfig)


class TestUser(TestCase):

    def setUp(self):
        context = test_app.app_context()
        context.push()

        self.db = test_db
        self.db.create_all()

        user1 = User(id=1, email='test1@test.com', username='test', password='test123')
        user2 = User(id=2, email='test2@test.com', username='test123', password='test123')
        user3 = User(id=3, email='test3@test.com', username='sometest', password='test123')
        user4 = User(id=4, email='test4@test.com', username='helloTest', password='test123')
        user5 = User(id=5, email='test5@test.com', username='helloworld', password='test123')
        user6 = User(id=6, email='test6@test.com', username='something', password='test123')

        self.db.session.add_all([user1, user2, user3, user4, user5, user6])
        self.db.session.commit()

        self.original_user = user1

        self.app = test_app.test_client()

    def tearDown(self):
        self.db.drop_all()

    def test_get_all_users(self):
        response = self.app.get('/api/user', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        users = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(users), list)
        self.assertEqual(len(users), 6)

        self.assertEqual(users[0], {
            'id': 1,
            'email': 'test1@test.com',
            'username': 'test'
        })

        self.assertEqual(users[2], {
            'id': 3,
            'email': 'test3@test.com',
            'username': 'sometest'
        })

    def test_get_user_by_id(self):
        response = self.app.get('/api/user/3', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        user = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(user), dict)
        self.assertEqual(user, {
            'id': 3,
            'email': 'test3@test.com',
            'username': 'sometest'
        })

        response = self.app.get('/api/user/6', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        user = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(user), dict)
        self.assertEqual(user, {
            'id': 6,
            'email': 'test6@test.com',
            'username': 'something'
        })

    def test_filter_users_by_username(self):
        response = self.app.get('/api/user/filter?username=test', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        users = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(users), list)
        self.assertEqual(len(users), 4)

        response = self.app.get('/api/user/filter?username=some', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        users = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(users), list)
        self.assertEqual(len(users), 2)

        response = self.app.get('/api/user/filter?username=world', headers=self.get_authorization_header(self.original_user))
        self.assertEqual(response.status_code, 200)

        users = json.loads(str(response.data, 'utf8'))
        self.assertEqual(type(users), list)
        self.assertEqual(len(users), 1)

    def get_authorization_header(self, user):
        auth_token = create_jwt(user)
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        return headers
