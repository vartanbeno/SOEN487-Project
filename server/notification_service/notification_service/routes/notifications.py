from flask import jsonify, Blueprint, request
from flask_cors import CORS
from flask_jwt_simple import jwt_required

from notification_service import db
from notification_service.helpers.jwt import get_user_id_from_jwt
from notification_service.helpers.response import response
from notification_service.models import Notification

notifications_api = Blueprint('notifications_api', __name__)
CORS(notifications_api)

@notifications_api.route('', methods=['GET'])
@jwt_required
def get_all_notifications():
    user_id = get_user_id_from_jwt()
    notifications = Notification.query.filter_by(receiverID=user_id)
    return jsonify([n.json() for n in notifications])

@notifications_api.route('', methods=['POST'])
@jwt_required
def put_notification():
    request_body = request.get_json()
    senderID = get_user_id_from_jwt()

    try:
        receiverID = int(request_body['receiverID'])
        message = request_body['message']
    except (ValueError, KeyError):
        return response('You must provide both receiver id and a message for your notification.', 400)

    notification = Notification(senderID=senderID, receiverID=receiverID, message=message)
    db.session.add(notification)
    db.session.commit()

    return response('Successfully sent notification.')

@notifications_api.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id).first()

    if notification is None or get_user_id_from_jwt() != notification.receiverID:
        response('You cannot delete a notification that is not yours.', 400)

    notification.delete()
    db.session.commit()

    return response('Successfully deleted notification.')
