import json
from unittest import TestCase

from app import create_app
from app.config import TestConfig

test_app = create_app(TestConfig)


class TestApp(TestCase):

    def setUp(self):
        self.app = test_app.test_client()

    def test_404_on_invalid_url(self):
        response = self.app.get("/notfound")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"message": "Page not found."})
