import json
from unittest import TestCase

from app import create_app, db as test_db
from app.config import TestConfig
from app.models import User, Verification

test_app = create_app(TestConfig)


class TestAuth(TestCase):

    def setUp(self):
        context = test_app.app_context()
        context.push()

        self.db = test_db
        self.db.create_all()

        self.app = test_app.test_client()

    def tearDown(self):
        self.db.drop_all()

    def test_register(self):
        user_count = User.query.count()
        verification_count = Verification.query.count()

        response = self.app.post("/api/auth/register", data=json.dumps(dict(
            email='test@test.com', username='test', password='test123'
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"message": "Successfully registered. Please verify your account."})

        self.assertEqual(User.query.count(), user_count + 1)
        self.assertEqual(Verification.query.count(), verification_count + 1)

    def test_verify(self):
        # first register a user, we can just use the registration test above
        self.test_register()

        verification_count = Verification.query.count()

        user = User.query.filter_by(username='test').first()
        verification = Verification.query.filter_by(user_id=user.id).first()

        response = self.app.post("/api/auth/verify?key=badkey")
        self.assertEqual(response.status_code, 400)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"message": "Invalid verification."})

        response = self.app.post(f"/api/auth/verify?key={verification.key}")
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"message": "You've successfully verified your account."})

        # a successful verification deletes its row from the verification table
        self.assertEqual(Verification.query.count(), verification_count - 1)

    def test_login(self):
        # first register a user and verify them, we can just use the verification test above
        self.test_verify()

        response = self.app.post("/api/auth/login", data=json.dumps(dict(
            username='test', password='incorrectpassword'
        )), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        body = json.loads(str(response.data, "utf8"))
        self.assertEqual(body, {"message": "Incorrect username and/or password."})

        response = self.app.post("/api/auth/login", data=json.dumps(dict(
            username='test', password='test123'
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertTrue('token' in body)
