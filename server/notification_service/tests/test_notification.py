import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import Person, Admin, NotificationType

tested_app.config.from_object(TestConfig)


class TestNotification(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(NotificationType(id=1, type = "email"))
        self.db.session.add(NotificationType(id=2, type = "phone"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        NotificationType.query.delete()
        self.db.session.commit()

    def test_get_all_notifications(self):
        response = self.app.get("/notifications")
        self.assertEqual(response.status_code, 200)

        notification_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(notification_list), list)
        self.assertDictEqual(notification_list[0], {'id': '1', 'type': 'email'})
        self.assertDictEqual(notification_list[1], {'id': '2', 'type': 'phone'})

    def test_put_notifications(self):
        # send the request and check the response status code
        response = self.app.put("/notifications", data={"type": "cellphone"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = NotificationType.query.filter_by(type="cellphone").count()
        self.assertEqual(updated_count, 1)

    def test_delete_notification(self):
        # do we really need to check counts?
        initial_count = NotificationType.query.filter_by(id=1).count()

        # send the request and check the response status code
        response = self.app.delete("/notifications/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = NotificationType.query.filter_by(id=1).count()
        self.assertEqual(updated_count, initial_count-1)

    def test_delete_admin_no_admin(self):
        response = self.app.delete("/notifications/100000")
        self.assertEqual(response.status_code, 406)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 406, "msg": "This notification type ID doesn't exist"})