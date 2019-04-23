from flask_jwt_simple import get_jwt, jwt_required
from ImgManager import jwt
from flask import jsonify, make_response


def get_user_id_from_jwt():
    return int(get_jwt()['sub'])


def get_email_from_jwt():
    return get_jwt()['email']


def get_username_from_jwt():
    return get_jwt()['username']


@jwt_required
def must_be_authenticated():
    pass


@jwt.expired_token_loader
def notify_token_expired():
    return make_response(jsonify({"code": "401", "msg": "Expired authentication token"}), 401)
