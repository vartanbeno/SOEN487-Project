from flask_jwt_simple import get_jwt, jwt_required

from messaging_service import jwt
from messaging_service.helpers.response import response


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


def get_token_from_authorization_header(request):
    return request.headers.get('Authorization').split()[1]


def get_authorization_header(token):
    return {
        'Authorization': f'Bearer {token}'
    }
