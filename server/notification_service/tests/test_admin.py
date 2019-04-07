import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import Person, Admin

tested_app.config.from_object(TestConfig)


class TestAdmin(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Person(id=1, name="Alice", password="Bob",email="alice@bob.com",notifications=True,notificationType="email"))
        self.db.session.add(Person(id=2, name="Bob",  password="Alice",email="aweesome@bob.com",notifications=True,notificationType="email"))
        self.db.session.add(Admin(id =1))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Admin.query.delete()
        Person.query.delete()
        self.db.session.commit()

    def test_get_all_admin(self):
        # send the request and check the response status code
        response = self.app.get("/admin")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        admin_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(admin_list), list)
        self.assertDictEqual(admin_list[0], {'id': '1'})

    def test_get_admin_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/admin/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        admin = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(admin, {'id': '1'})

    def test_get_person_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/admin/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this person id."})

    def test_delete_admin(self):
        # do we really need to check counts?
        initial_count = Admin.query.filter_by(id=1).count()

        # send the request and check the response status code
        response = self.app.delete("/admin/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Admin.query.filter_by(id=1).count()
        self.assertEqual(updated_count, initial_count-1)

    def test_delete_admin_no_admin(self):
        response = self.app.delete("/admin/100000")
        self.assertEqual(response.status_code, 406)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 406, "msg": "This person cannot be deleted"})


