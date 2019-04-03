from datetime import datetime

from flask import current_app, jsonify
from flask_jwt_simple import create_jwt, get_jwt, jwt_required

from app import jwt
from app.helpers.response import response


@jwt.jwt_data_loader
def generate_jwt(user):
    now = datetime.utcnow()
    return {
        'exp': now + current_app.config['JWT_EXPIRES'],
        'iat': now,
        'nbf': now,
        'sub': user.id,
        'email': user.email,
        'username': user.username
    }


def token(user):
    return jsonify({'token': create_jwt(user)})


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
