from flask_jwt_simple import get_jwt, jwt_required

from app import jwt
from app.helpers.response import response


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
    return response('Your authentication token has expired.', 401)
