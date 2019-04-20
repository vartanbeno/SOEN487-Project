import secrets
import os
import jwt
import io
from PIL import Image
from flask import jsonify, make_response, request
from ImgManager import app, db, bcrypt
from ImgManager.models import row2dict, Client, Album, Image
from ImgManager.JWT_handler import get_username_from_jwt
from flask_jwt_simple import jwt_required


# TODO SET WEBSITE NAME OR IP ADDRESS
_domain_name = ""


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route("/img", methods={"POST"})
@jwt_required
def upload_img():
    client = get_username_from_jwt()
    album = request.form.get("album")
    form_picture = request.files['image']

    # verify existence of client or create new and add to DB
    verify_client(client)

    # validate album or create new album for client
    if not album:
        album = "default"

    verify_album(album, client)

    if not form_picture:
        return make_response(jsonify({"code": 403, "msg": "Invalid fields"}), 403)

    # taken from Corey M. Schafer code snippets
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    local_path = os.path.join(app.root_path + '\Images', picture_fn)

    # making sure the random hex hasn't already been produced
    while os.path.exists(local_path):
        print("Creating new hex")
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        local_path = os.path.join(app.root_path + '\Images', picture_fn)

    # if valid save picture with a valid path
    i = Image.open(form_picture)
    i.save(local_path)

    picture_path = _domain_name + "/" + 'Images' + "/" + picture_fn

    new_pic = Image(album_id=album, path=picture_path)
    db.session.add(new_pic)
    db.session.commit()

    return jsonify({"code": 200, "msg": "success", "path": f"{picture_path}"})


def verify_client(user):
    a_user = Client.query.filter_by(name=user).first()

    if not a_user:
        a_user = Client(name=user)
        db.session.add(user)
        db.session.commit()

    return a_user


def verify_album(an_album, user):
    # retrieve all album
    album_objs = Album.query.filter_by(album=an_album)

    for alb in album_objs:
        if alb.client_id is user.id:
            return alb

    album = Album(name=an_album, client_id=user.id)

    return album