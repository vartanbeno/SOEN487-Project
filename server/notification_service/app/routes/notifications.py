import sqlalchemy
from flask import jsonify, Blueprint, make_response, request
from sqlalchemy import exc
from flask_cors import CORS
from flask_jwt_simple import jwt_required
from app.helpers.jwt import get_user_id_from_jwt

from app import models
from app.helpers.jwt import must_be_authenticated

notifications_api = Blueprint('notifications_api', __name__)

CORS(notifications_api)

@notifications_api.route("/")
@jwt_required
def get_all_notifications():
    n_list = models.Notification.query.all()
    return jsonify([models.row2dict(notification) for notification in n_list])

@notifications_api.route("/user/<userID>", methods={"GET"})
def get_by_receiverID(userID):
    messages = models.Notification.query.filter_by(receiverID = userID)
    return jsonify([models.row2dict(notification) for notification in messages])

@notifications_api.route("/", methods={"PUT"})
@jwt_required
def put_notification():
    print("started")
    senderID = get_user_id_from_jwt()
    print(request.get_json())

    receiverID = request.get_json().get('receiverID')
    message = request.get_json().get('message')
    print(type(senderID))
    print(type(receiverID))
    print(type(message))
    if not senderID:
        return make_response(jsonify({"code": 403,"msg": "Cannot put notification. Missing sender ID."}), 403)
    if not receiverID:
        return make_response(jsonify({"code": 403, "msg": "Cannot put notification. Missing receiver ID."}), 403)
    if not message:
        return make_response(jsonify({"code": 403, "msg": "Cannot put notification. Missing message."}), 403)

    notification = models.Notification(senderID= senderID, receiverID= receiverID, message=message)

    #start insert transaction
    models.db.session.add(notification)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        error = "Cannot put notification."
        print("SQL error")
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})

@notifications_api.route("/<n_id>", methods={"DELETE"})
def delete_notification(n_id):
    notification = models.Notification.query.filter_by(id = n_id).first()

    if notification:
        models.Notification.query.filter_by(id=n_id).delete()
    else:
        return make_response(jsonify({"code": 406, "msg": "This notification ID doesn't exist"}), 406)

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete notification. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})
