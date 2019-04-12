import unittest
import json

import app as tested_app
from app.config import TestConfig

tested_app = tested_app.create_app(TestConfig)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()

    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"message": "Page not found."})
