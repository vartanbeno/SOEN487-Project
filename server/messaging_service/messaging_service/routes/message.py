import requests
from flask import Blueprint, request
from flask_jwt_simple import jwt_required

from messaging_service import db
from messaging_service.helpers.jwt import get_user_id_from_jwt, get_token_from_authorization_header, \
    get_authorization_header
from messaging_service.helpers.response import response
from messaging_service.models import Conversation, Message

message_api = Blueprint('message_api', __name__)


@message_api.route('', methods=['POST'])
@jwt_required
def create_message():
    user_id = get_user_id_from_jwt()
    request_body = request.get_json()

    if 'conversation_id' not in request_body or 'text' not in request_body:
        return response('You must provide both conversation id and message text.', 400)

    conversation_id = int(request_body['conversation_id'])
    text = request_body['text']

    conversation = Conversation.query.filter_by(id=conversation_id).first()
    if conversation is None or (user_id != conversation.creator_id and user_id != conversation.participant_id):
        return response('You are not part of this conversation.', 400)

    receiver_id = conversation.creator_id if user_id == conversation.participant_id else conversation.participant_id

    message = Message(conversation_id=conversation.id, sender_id=user_id, text=text)
    db.session.add(message)
    db.session.commit()

    token = get_token_from_authorization_header(request)
    auth_header = get_authorization_header(token)
    requests.put(
        'http://localhost:8080/api/notifications',
        json={
            'receiverID': receiver_id,
            'message': f'You have a new message from {user_id}.'
        },
        headers=auth_header
    )

    return response('Successfully sent message.')
