import json
from unittest import TestCase
from app import create_app
from app import db as tested_db
from app.config import TestConfig
from app.models import Notification

tested_app = create_app(TestConfig)


class TestNotification(TestCase):
    def setUp(self):
        context = tested_app.app_context()
        context.push()

        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Notification(senderID = 1, receiverID=2, message="test message 1"))
        self.db.session.add(Notification(senderID = 2, receiverID=1, message="test message 2"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Notification.query.delete()
        self.db.session.commit()

    def test_get_all_notifications(self):
        response = self.app.get("/notifications")
        self.assertEqual(response.status_code, 200)

        notification_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(notification_list), list)

    def test_put_notifications(self):
        # send the request and check the response status code
        response = self.app.put("/notifications", data={"senderID": "4", "receiverID": "2", "message": "Testing if this works"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Notification.query.count()
        self.assertEqual(updated_count, 1)

    def test_delete_notification(self):

        initial_count = Notification.query.filter_by(id=1).count()

        # send the request and check the response status code
        response = self.app.delete("/notifications/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Notification.query.filter_by(id=1).count()
        self.assertEqual(updated_count, initial_count-1)



