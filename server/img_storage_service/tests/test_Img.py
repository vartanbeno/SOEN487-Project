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
from ImgManager.models import Client, Album, Img
# tested_app.config.from_object(TestConfig)


_Token_identification_string = "Bearer"

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
        Img.query.delete()
        self.db.session.commit()

    def test_IMG_call(self):
        """
        Test Valid API CALL to ADD a Client, Album and IMG
        :return:
        """
        init_img_count = Img.query.count()
        init_cli_count = Client.query.count()
        init_alb_count = Album.query.count()

        now = int(time.time())

        album = "testAlb1"
        token = {"iss": "https://soen487.concordia.ca",
                 "iat": now,
                 "exp": now + 3600 * 2,
                 "user_id": 1,
                 "email": "fuckthatshieeettt"
                 }

        token = jwt.encode(token, tested_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        token = token.decode("utf-8")
        final_token = json.dumps({f"{_Token_identification_string}": token})

        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        response = self.app.post("/img", content_type='multipart/form-data',
                                 headers={"Authorization": final_token},
                                 data={"album": f"{album}", 'image': (img_bytes_io, 'test_img.jpg')})

        self.assertEqual(init_cli_count + 1, Client.query.count())
        self.assertEqual(init_alb_count + 1, Album.query.count())
        self.assertEqual(init_img_count + 1, Img.query.count())

    def test_no_album_IMG_Call(self):
        """
        Test Valid API CALL to ADD a Client, Album and IMG should Auto create a default Album.
        :return:
        """
        init_img_count = Img.query.count()
        init_cli_count = Client.query.count()
        init_alb_count = Album.query.count()

        now = int(time.time())

        token = {"iss": "https://soen487.concordia.ca",
                 "iat": now,
                 "exp": now + 3600 * 2,
                 "user_id": 1,
                 "email": "fuckthatshieeettt"
                 }

        token = jwt.encode(token, tested_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        token = token.decode("utf-8")
        final_token = json.dumps({f"{_Token_identification_string}": token})

        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        response = self.app.post("/img", content_type='multipart/form-data',
                                 headers={"Authorization": final_token},
                                 data={'image': (img_bytes_io, 'test_img.jpg')})

        self.assertEqual(init_cli_count + 1, Client.query.count())
        self.assertEqual(init_alb_count + 1, Album.query.count())
        self.assertEqual(init_img_count + 1, Img.query.count())

    def test_no_JWT_IMG_call(self):
        """
        Test Valid API CALL to ADD a Client, Album and IMG should Auto create a default Album.
        :return:
        """
        init_img_count = Img.query.count()
        init_cli_count = Client.query.count()
        init_alb_count = Album.query.count()

        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        response = self.app.post("/img", content_type='multipart/form-data',
                                 data={'image': (img_bytes_io, 'test_img.jpg')})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(init_cli_count, Client.query.count())
        self.assertEqual(init_alb_count, Album.query.count())
        self.assertEqual(init_img_count, Img.query.count())

    def test_valid_delete_img(self):

        now = int(time.time())
        # generate valid token
        token = {"iss": "https://soen487.concordia.ca",
                 "iat": now,
                 "exp": now + 3600 * 2,
                 "user_id": 1,
                 "email": "fuckthatshieeettt"
                 }
        token = jwt.encode(token, tested_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        token = token.decode("utf-8")
        final_token = json.dumps({f"{_Token_identification_string}": token})

        # get valid img
        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        # send request
        response = self.app.post("/img", content_type='multipart/form-data', headers={"Authorization": final_token},
                                 data={'image': (img_bytes_io, 'test_img.jpg')})

        # extract path from response
        json_resp = json.loads(str(response.data, "utf8"))
        path = json_resp['msg']

        # get count of pic
        pic_count = Img.query.count()

        response = self.app.delete("/img", headers={"Authorization": final_token}, data={"path": f'{path}'})
        self.assertEqual(response.status_code, 200)

        final_pic_count = Img.query.count()
        self.assertEqual(pic_count - 1, final_pic_count)

        self.assertEqual(False, os.path.exists(os.getcwd() + ".." + "Images" + "/" + 'test_img.jpg'))

    def test_missing_token_delete_img(self):
        now = int(time.time())
        # generate valid token
        token = {"iss": "https://soen487.concordia.ca",
                 "iat": now,
                 "exp": now + 3600 * 2,
                 "user_id": 1,
                 "email": "fuckthatshieeettt"
                 }
        token = jwt.encode(token, tested_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        token = token.decode("utf-8")
        final_token = json.dumps({f"{_Token_identification_string}": token})

        # get valid img
        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        # send request
        response = self.app.post("/img", content_type='multipart/form-data', headers={"Authorization": final_token},
                                 data={'image': (img_bytes_io, 'test_img.jpg')})

        # extract path from response
        json_resp = json.loads(str(response.data, "utf8"))
        path = json_resp['msg']

        response = self.app.delete("/img", data={"path": f'{path}'})
        self.assertEqual(response.status_code, 403)

    def test_no_path_delete(self):

        now = int(time.time())
        # generate valid token
        token = {"iss": "https://soen487.concordia.ca",
                 "iat": now,
                 "exp": now + 3600 * 2,
                 "user_id": 1,
                 "email": "fuckthatshieeettt"
                 }
        token = jwt.encode(token, tested_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        token = token.decode("utf-8")
        final_token = json.dumps({f"{_Token_identification_string}": token})

        # get valid img
        with open('test_img.jpg', 'rb') as img1:
            try:
                img_bytes_io = io.BytesIO(img1.read())
            except:
                print("File can't be read.")

        # send request
        response = self.app.post("/img", content_type='multipart/form-data', headers={"Authorization": final_token},
                                 data={'image': (img_bytes_io, 'test_img.jpg')})

        # extract path from response
        json_resp = json.loads(str(response.data, "utf8"))
        path = json_resp['msg']

        # get count of pic
        pic_count = Img.query.count()

        response = self.app.delete("/img", headers={"Authorization": final_token})
        self.assertEqual(response.status_code, 404)

        final_pic_count = Img.query.count()
        self.assertEqual(pic_count, final_pic_count)
