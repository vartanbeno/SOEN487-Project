import secrets
import os
import jwt
import json
from PIL import Image
from flask import jsonify, make_response, request
from ImgManager import app, db, bcrypt
from ImgManager.models import row2dict, Client, Album, Img



# TODO SET WEBSITE NAME/IP ADDRESS and port #?
_domain_name = ""
_Token_identification_string = "Bearer"


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route("/")
def greet():
    return make_response(jsonify({"code": 200, "msg": "Uploading some img?"}), 200)


@app.route("/img", methods={"POST"})
def upload_img():
    """
    When posting a http request with a valid image and an optional album attribute
    :return: success code and the path of the msg
    """

    # validate token
    try:
        token = json.loads(request.headers['Authorization'])
    except:
        return make_response(jsonify({"code": 403, "msg": "Signature is expired"}), 403)

    # try decoding the token, if any errors, make 403 response, else
    try:
        decoded = jwt.decode(token[_Token_identification_string], app.config['JWT_SECRET_KEY'], algorithm="HS256")
    except jwt.ExpiredSignatureError:
        return make_response(jsonify({"code": 403, "msg": "Signature is expired"}), 403)
    except jwt.InvalidTokenError:
        return make_response(jsonify({"code": 403, "msg": "Your token is not valid"}), 403)

    # Extract information from http Request
    client = decoded['email']
    album = request.form.get("album")
    form_picture = request.files['image']

    # verify existence of client or create new and add to DB
    client = verify_client(client)
    client = Client.query.filter_by(name=client.name).first()

    # validate album or create new album for client
    if not album:
        album = "default"

    # verify that the album exists or create it
    album = verify_album(album, client)

    # verify that the picture in the form is there
    if not form_picture:
        return make_response(jsonify({"code": 400, "msg": "Invalid fields"}), 400)

    # taken from Corey M. Schafer code snippets, create random file name for the saved images
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

    # commit picture information to DB
    picture_path = _domain_name + "/" + 'Images' + "/" + picture_fn
    new_pic = Img(album_id=album.id, path=picture_path)
    db.session.add(new_pic)
    db.session.commit()

    return make_response(jsonify({"code": 200, "msg": f"{picture_path}"}))


@app.route("/img", methods={'DELETE'})
def delete_pic():
    """
    Method requiring valid JWT and a path str
    :return: http responses with different code depending on the validity of the request
    """

    # validate token
    try:
        token = json.loads(request.headers['Authorization'])
    except:
        return make_response(jsonify({"code": 403, "msg": "Signature is expired"}), 403)

    # try decoding the token, if any errors, make 403 response, else
    try:
        decoded = jwt.decode(token[_Token_identification_string], app.config['JWT_SECRET_KEY'], algorithm="HS256")
    except jwt.ExpiredSignatureError:
        return make_response(jsonify({"code": 403, "msg": "Signature is expired"}), 403)
    except jwt.InvalidTokenError:
        return make_response(jsonify({"code": 403, "msg": "Your token is not valid"}), 403)

    # Extract information from http Request
    client = decoded['email']

    # check if client exists, if not he can't delete anything
    a_user = Client.query.filter_by(name=client).first()
    if not a_user:
        return make_response(jsonify({"code": 400, "msg": "Invalid request"}), 400)

    # get img to delete path
    path = request.form.get("path")

    if not path:
        return make_response(jsonify({"code": 404, "msg": "Can't find requested Image"}), 404)

    # retrieve path
    target_pic = Img.query.filter_by(path=path).first()

    # check if picture exists
    if not target_pic:
        return make_response(jsonify({"code": 404, "msg": "Can not find requested Image"}), 404)

    # find the picture album
    target_pic_albid = target_pic.album_id
    target_pic_album = Album.query.filter_by(id=target_pic_albid).first()

    # make sure the album belongs to the user
    if not target_pic_album.client_id == a_user.id:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)

    # create relative path for removal
    img_stored_name = target_pic.path.split("/")[-1]
    absolute_path = os.getcwd() + "/" + "images" + "/" + img_stored_name

    # verify path existence and remove img
    if os.path.exists(absolute_path):
        try:
            os.remove(absolute_path)
        except OSError:
            pass

    # commit changes
    db.session.delete(target_pic)
    db.session.commit()
    return make_response(jsonify({"code": 200, "msg": "success"}))


def verify_client(user):
    """
    used to verify user presence in the DB
    :param user: Client name as a String
    :return: Client OBJ
    """
    a_user = Client.query.filter_by(name=user).first()

    if not a_user:
        a_user = Client(name=user)
        db.session.add(a_user)
        db.session.commit()

    return Client.query.filter_by(name=user).first()


def verify_album(an_album, user):
    """
    :param an_album: Album name as a String
    :param user: Client OBJ
    :return: Album Obj
    """
    album_objs = Album.query.filter_by(name=an_album)

    for alb in album_objs:
        if alb.client_id == user.id:
            return alb

    album = Album(name=an_album, client_id=user.id)
    db.session.add(album)
    db.session.commit()

    return album
