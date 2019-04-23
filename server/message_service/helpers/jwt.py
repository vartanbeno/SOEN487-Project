import jwt
from flask import current_app


def get_data_from_token(token):
    try:
        decode = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise Exception("Signature expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    return decode

