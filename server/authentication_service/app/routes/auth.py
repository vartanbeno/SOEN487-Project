from flask import Blueprint, request, jsonify
import json
from sqlalchemy import func

from app import db
from app.helpers.bcrypt import hashpw, matches
from app.helpers.jwt import token
from app.helpers.response import response
from app.models import User, Verification

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/register', methods=['POST'])
def register():
    """
    Registers a user in the database. We return a 400 response if:
        - a user with the provided username already exists
        - no password is provided
        - validation of the user's credentials fails
    :return: Response object
    """
    data = request.get_json()

    if not data.get('password'):
        return response("Must provide a password.", 400)

    user = User.query.filter(func.lower(User.username) == func.lower(data.get('username'))).first()
    if user is not None:
        return response(f'A user with the username {user.username} already exists.', 400)

    user = User(
        email=data.get('email'),
        username=data.get('username'),
        password=hashpw(data.get('password'))
    )

    try:
        user.validate()
    except Exception as e:
        return response(e, 400)

    db.session.add(user)
    db.session.flush()

    verification = Verification(user_id=user.id)
    verification.generate_random_key()

    # In case the randomly generated key isn't unique (very low likelihood as it's 200 characters long), regenerate it
    while Verification.query.filter_by(key=verification.key).first() is not None:
        verification.generate_random_key()

    db.session.add(verification)
    db.session.commit()

    return response("Successfully registered. Please verify your account.")


@auth_api.route('/login', methods=['POST'])
def login():
    """
    Logs user in by providing a JSON web token. We return a 400 response if:
        - the user has not verified their account yet
        - incorrect credentials are provided
    :return: Response object or token
    """
    data = request.get_json()
    user = User.query.filter(func.lower(User.username) == func.lower(data.get('username'))).first()

    if user is not None and not user.is_verified():
        return response('You cannot log in if your account is not verified.', 400)
    elif user is not None and matches(data.get('password'), user.password):
        return token(user)
    else:
        return response('Incorrect username and/or password.', 400)


@auth_api.route('/verify', methods=['GET', 'POST'])
def verify():
    """
    We extract the key argument from the request URL (?key=[key]) and check if it exists in the verification table.
    If it doesn't, we return a 400 response.
    If it does, we delete the verification entity from the database, breaking its relationship with its user.
    :return: Response object
    """
    print('made it to verify')

    key = request.args.get('key')

    print('the key is '+str(key))
    verification = Verification.query.filter_by(key=key).first()
    print(verification)

    if verification is not None:
        db.session.delete(verification)
        db.session.commit()
        return response('You\'ve successfully verified your account.')
    else:
        return response('Invalid verification.', 400)
