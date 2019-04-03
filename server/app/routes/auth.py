from flask import Blueprint, request
from sqlalchemy import func

from app import db
from app.helpers.bcrypt import hashpw
from app.helpers.response import response
from app.models import User, Verification

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/register', methods=['POST'])
def register():
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

    db.session.add(verification)
    db.session.commit()

    return response("Successfully registered! Please verify your account.")
