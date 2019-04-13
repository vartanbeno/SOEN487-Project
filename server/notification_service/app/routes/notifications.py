import sqlalchemy
from flask import jsonify, Blueprint, make_response, request
from sqlalchemy import exc

from app import models
from app.helpers.jwt import must_be_authenticated

notifications_api = Blueprint('notifications_api', __name__)
notifications_api.before_request(must_be_authenticated)

@notifications_api.route("/")
def get_all_notifications():
    n_list = models.Notification.query.all()
    return jsonify([models.row2dict(notification) for notification in n_list])

@notifications_api.route("/", methods={"PUT"})
def put_notification():
    nType = request.form.get("type")

    if not nType:
        return make_response(jsonify({"code": 403,"msg": "Cannot put notification type. Missing mandatory fields."}), 403)
    n_id = request.form.get("id")
    if not n_id:
        p = models.Notification(type = nType)
    else:
        p = models.Notification(id=n_id, type = nType)

    #start insert transaction
    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        error = "Cannot put notification."
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})

@notifications_api.route("/<n_id>", methods={"DELETE"})
def delete_notification(n_id):
    nType = models.Notification.query.filter_by(id = n_id).first()

    if nType:
        models.Notification.query.filter_by(id=n_id).delete()
    else:
        return make_response(jsonify({"code": 406, "msg": "This notification type ID doesn't exist"}), 406)

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete notification type. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})
