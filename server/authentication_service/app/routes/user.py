from flask import Blueprint, jsonify, request


from app.helpers.response import response
from app.models import User

from flask_cors import CORS
from flask_jwt_simple import jwt_required

user_api = Blueprint('user_api', __name__)


CORS(user_api)


@user_api.route('', methods=['GET'])
@jwt_required
def get_all_users():
    users = User.query.all()
    return jsonify([user.json() for user in users])


@user_api.route('/<int:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return response(f'User with id {user_id} not found.', 404)
    else:
        return jsonify(user.json())


@user_api.route('/filter', methods=['GET'])
@jwt_required
def filter_users_by_username():
    """
    Get list of users whose username contains the username request parameter (?username=[username]).
    We make sure to strip() the username parameter, i.e. remove any whitespace on the left and right.
    We also convert it to lowercase and compare it with all actual username also converted to lowercase.
    :return: list of users with username request parameter in their username
    """
    username = request.args.get('username').strip().lower()
    users = User.query.all()
    users = [user for user in users if username in user.username.lower()]
    return jsonify([user.json() for user in users])
