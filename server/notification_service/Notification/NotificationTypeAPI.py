import sqlalchemy
from flask import jsonify, Blueprint, make_response, request

import models
from main import app

nBp = Blueprint('nBp', __name__)

@nBp.route("/notifications")
def get_all_notifications():

    auth_token = extractToken(request.headers.get('Authorization'))

    if not auth_token:
        return jsonify("message","Please login to access this resource")
    else:
        n_list = models.NotificationType.query.all()
        return jsonify([models.row2dict(notification) for notification in n_list])

@nBp.route("/notifications", methods={"PUT"})
def put_notification():

    auth_token = extractToken(request.headers.get('Authorization'))

    if not auth_token:
        return jsonify("message", "Please login to access this resource")
    else:
        nType = request.form.get("type")

        if not nType:
            return make_response(jsonify({"code": 403,"msg": "Cannot put notification type. Missing mandatory fields."}), 403)
        n_id = request.form.get("id")
        if not n_id:
            p = models.NotificationType(type = nType)
        else:
            p = models.NotificationType(id=n_id, type = nType)

        #start insert transaction
        models.db.session.add(p)
        try:
            models.db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot put notification. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "success"})

@nBp.route("/notifications/<n_id>", methods={"DELETE"})
def delete_notification(n_id):
    auth_token = extractToken(request.headers.get('Authorization'))

    if not auth_token:
        return jsonify("message", "Please login to access this resource")
    else:

        nType = models.NotificationType.query.filter_by(id = n_id).first()

        if nType:
            models.NotificationType.query.filter_by(id=n_id).delete()
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


def extractToken(auth_header):

    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
        return auth_token
    else:
        auth_token = ''
        return auth_token