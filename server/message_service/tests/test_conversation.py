import unittest
import json
import jwt
import time
import os
from app import app as tested_app
from app import db as tested_db
from config import TestConfig
from models import Conversation, Message

tested_app.config.from_object(TestConfig)


class TestConversation(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Conversation(creator_id=1, participant_id=3))
        self.db.session.add(Conversation(creator_id=2, participant_id=4))
        self.db.session.add(Message(conversation_id=1, sender_id=1, text="test1"))
        self.db.session.add(Message(conversation_id=1, sender_id=1, text="test2"))
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
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Conversation.query.delete()
        Message.query.delete()
        self.db.session.commit()

    def test_get_all_conversations(self):
        response = self.app.get("/conversation", headers={'Authorization':self.authorization_token})
        self.assertEqual(response.status_code, 200)

        conversations = json.loads(str(response.data, "utf8"))
        print(conversations)
        self.assertEqual(type(conversations), dict)
        self.assertDictEqual(conversations['conversations'][0], {"creator_id": "1", "participant_id": "3", "id":"1"})
        self.assertEqual(len(conversations['conversations']), 1)

    def test_post_conversation(self):
        initial_count = Conversation.query.filter_by(participant_id=3).count()

        response = self.app.post(
            "/conversation",
            json={"participant_id": "3"},
            headers={'Authorization': self.authorization_token})
        print(response.status_code)
        self.assertEqual(response.status_code, 201)

        updated_count = Conversation.query.filter_by(participant_id=3).count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_get_conversation(self):
        response = self.app.get("/conversation/1", headers={'Authorization':self.authorization_token})
        self.assertEqual(response.status_code, 200)

        conversation = json.loads(str(response.data, "utf8"))
        # print(conversation)
        self.assertDictEqual(conversation, {"id": 1, "creator_id": 1, "messages": [], "participant_id": 3})

    def test_get_conversation_with_message_limit(self):
        response = self.app.get("/conversation/1/1", headers={'Authorization':self.authorization_token})
        self.assertEqual(response.status_code, 200)

        conversation = json.loads(str(response.data, "utf8"))
        self.assertEqual(conversation['id'], 1)
        self.assertEqual(conversation['creator_id'], 1)
        self.assertEqual(conversation['participant_id'], 3)
        self.assertEqual(conversation['messages'][0]['conversation_id'],"1")
        self.assertEqual(conversation['messages'][0]['id'], "2")
        self.assertEqual(conversation['messages'][0]['sender_id'], "1")
        self.assertEqual(conversation['messages'][0]['text'], "test2")


if __name__ == '__main__':
    unittest.main()
