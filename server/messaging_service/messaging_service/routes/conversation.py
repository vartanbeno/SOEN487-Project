import requests

from flask import Blueprint, jsonify, request
from flask_jwt_simple import jwt_required

from messaging_service import db
from messaging_service.helpers.jwt import get_user_id_from_jwt, get_token_from_authorization_header, \
    get_authorization_header
from messaging_service.helpers.response import response
from messaging_service.models import Conversation, Message

conversation_api = Blueprint('conversation_api', __name__)


@conversation_api.route('', methods=['GET'])
@jwt_required
def get_conversations():
    user_id = get_user_id_from_jwt()

    conversations = list(Conversation.query.filter_by(creator_id=user_id))
    conversations_participating = list(Conversation.query.filter_by(participant_id=user_id))
    conversations.extend(conversations_participating)

    return jsonify([c.json() for c in conversations])


@conversation_api.route('<int:conversation_id>', methods=['GET'])
@jwt_required
def get_messages(conversation_id):
    user_id = get_user_id_from_jwt()
    conversation = Conversation.query.filter_by(id=conversation_id).first()

    if conversation is None or user_id != conversation.creator_id or user_id != conversation.participant_id:
        return response('You are not part of this conversation.', 400)

    messages = Message.query.filter_by(conversation_id=conversation.id)
    return jsonify(m.json() for m in messages)


@conversation_api.route('<int:conversation_id>/limit/<int:message_limit>', methods=['GET'])
@jwt_required
def get_messages_with_limit(conversation_id, message_limit):
    user_id = get_user_id_from_jwt()
    conversation = Conversation.query.filter_by(id=conversation_id).first()

    if conversation is None or (user_id != conversation.creator_id and user_id != conversation.participant_id):
        return response('You are not part of this conversation.', 400)

    messages = Message.query.filter_by(conversation_id=conversation.id).limit(message_limit)
    return jsonify(m.json() for m in messages)


@conversation_api.route('', methods=['POST'])
@jwt_required
def create_conversation():
    user_id = get_user_id_from_jwt()

    try:
        participant_id = int(request.get_json()['participant_id'])
    except (ValueError, KeyError):
        return response('You must provide a valid participant id (only digits).', 400)

    if user_id == participant_id:
        return response('You cannot create a conversation with yourself.', 400)

    token = get_token_from_authorization_header(request)
    auth_header = get_authorization_header(token)
    res = requests.get(f'http://localhost:5000/api/user/{participant_id}', headers=auth_header)

    if res.status_code == 404:
        return response('This user does not exist.', 400)
    elif res.status_code == 401:
        return response('Invalid authorization token.', 401)

    conversation = Conversation(creator_id=user_id, participant_id=participant_id)
    db.session.add(conversation)
    db.session.commit()

    return response('Successfully created conversation.')
