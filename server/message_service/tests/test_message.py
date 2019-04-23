import unittest
import jwt
import time
import requests_mock
from app import app as tested_app
from app import db as tested_db
from config import TestConfig
from models import Message

tested_app.config.from_object(TestConfig)


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Message(conversation_id=1, sender_id=1, text="message_text"))
        self.db.session.commit()
        now = int(time.time())
        token = {
            'exp': now + 86400,
            'iat': now,
            'nbf': now,
            'sub': 1,
            'email': "test@test.ca",
            'username': "giovanni"
        }
        token = jwt.encode(token, TestConfig.JWT_SECRET_KEY, algorithm="HS256")
        self.authorization_token = "Bearer {}".format(token.decode("utf8"))

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Message.query.delete()
        self.db.session.commit()

    def test_post_message(self):
        initial_count = Message.query.filter_by(conversation_id=2).count()
        with requests_mock.Mocker() as m:
            m.put('http://127.0.0.1:8080/api/notifications/', text='good')
            response = self.app.post(
                "/message",
                json={"conversation_id":2, "sender_id":2, "text":"blabla"},
                headers={'Authorization':self.authorization_token}
            )
        self.assertEqual(response.status_code, 201)

        updated_count = Message.query.filter_by(conversation_id=2).count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_delete_message(self):
        initial_count = Message.query.filter_by(conversation_id=1).count()

        response = self.app.delete("/message/1", headers={'Authorization':self.authorization_token})
        self.assertEqual(response.status_code, 202)

        updated_count = Message.query.filter_by(conversation_id=1).count()
        self.assertEqual(updated_count, initial_count - 1)


if __name__ == '__main__':
    unittest.main()
