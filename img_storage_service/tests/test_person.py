import unittest
import json
import time
from flask import jsonify
from flask_jwt_simple import create_jwt, get_jwt, jwt_required
import jwt
import io
import os
from ImgManager import app as tested_app
from ImgManager import db as tested_db
from ImgManager.models import Client, Album, Image
# tested_app.config.from_object(TestConfig)


class TestPerson(unittest.TestCase):
    def setUp(self):
        context = tested_app.app_context()
        context.push()
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Client.query.delete()
        Album.query.delete()
        Image.query.delete()
        self.db.session.commit()

    def test_API_call(self):
        init_img_count = Image.query.count()
        init_cli_count = Client.query.count()
        init_alb_count = Album.query.count()

        now = int(time.time())

        token = {
        'exp': now + 3600 * 2,
        'iat': now,
        'nbf': now,
        'sub': 1,
        'email': "test@email.com",
        'username': "testyBoii"
        }

        token1 = create_jwt(token)
        header_token = jsonify({'token': create_jwt(token)})
        album = "testAlb1"

        print(header_token)
        print('Wot?')
        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")
        print("wot2?")

        test = jwt.decode(token1, tested_app.config['JWT_SECRET_KEY'])
        print("wot3?")

        response = self.app.post("/img", content_type='multipart/form-data',
                                 headers={"Authorization": token},
                                 data={"album": f"{album}", 'image': (img_bytes_io, 'test_img.jpg')})

        print(response)

        self.assertEqual(init_cli_count + 1, Client.query.count())
        self.assertEqual(init_alb_count + 1, Album.query.count())
        self.assertEqual(init_img_count + 1, Image.query.count())

