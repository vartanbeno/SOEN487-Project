import sqlalchemy
from flask import jsonify, Blueprint, make_response

import models
from main import app

adminBp = Blueprint('adminBp', __name__)

@adminBp.route("/admin")
def get_all_admin():
    admin_list = models.Admin.query.all()
    return jsonify([models.row2dict(admin) for admin in admin_list])

@adminBp.route("/admin/<admin_id>")
def get_admin(admin_id):
    # id is a primary key, so we'll have max 1 result row
    admin = models.Admin.query.filter_by(id=admin_id).first()
    if admin:
        return jsonify(models.row2dict(admin))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)

@adminBp.route("/admin/<admin_id>", methods={"DELETE"})
def delete_admin(admin_id):

    admin = models.Admin.query.filter_by(id = admin_id).first()

    if admin:
        models.Admin.query.filter_by(id=admin_id).delete()
    else:
        return make_response(jsonify({"code": 406, "msg": "This person cannot be deleted"}), 406)

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete admin. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})