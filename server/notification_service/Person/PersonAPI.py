import sqlalchemy
from flask import jsonify, Blueprint, make_response, request

import models
from main import app

personBp = Blueprint('personBp', __name__)

@personBp.route("/person")
def get_all_person():
    person_list = models.Person.query.all()
    return jsonify([models.row2dict(person) for person in person_list])


@personBp.route("/person/<person_id>")
def get_person(person_id):
    # id is a primary key, so we'll have max 1 result row
    person = models.Person.query.filter_by(id=person_id).first()
    if person:
        return jsonify(models.row2dict(person))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)


@personBp.route("/person", methods={"PUT"})
def put_person():
    # get the name first, if no name then fail
    name = request.form.get("name")
    password = request.form.get("password")
    email = request.form.get("email")
    notifications = bool(request.form.get("notifications"))
    n = request.form.get("notificationType")

   # if not name or password or email or notifications or n:
    #    return make_response(jsonify({"code": 403,"msg": "Cannot put person. Missing mandatory fields."}), 403)
    person_id = request.form.get("id")
    if not person_id:
        p = models.Person(name=name,password=password,email=email,notifications=notifications, notificationType=n)
    else:
        p = models.Person(id=person_id, name=name, password=password,email=email,notifications=notifications, notificationType=n)

    #start insert transaction
    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})