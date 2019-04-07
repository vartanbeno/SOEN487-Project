import sqlalchemy
from flask import jsonify, Blueprint, make_response, request

import models
from main import app

nBp = Blueprint('nBp', __name__)

@nBp.route("/notifications")
def get_all_notifications():
    n_list = models.NotificationType.query.all()
    return jsonify([models.row2dict(notification) for notification in n_list])

@nBp.route("/notifications", methods={"PUT"})
def put_notification():

    nType = request.form.get("type")
    #print('NTYPE IS : '+nType+' with type : ')
    #print(type(nType))

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
def delete_admin(n_id):

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