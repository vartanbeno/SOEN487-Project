from flask import Flask, jsonify, make_response
from config import DevConfig

# need an app before we import models because models need it
app = Flask(__name__)
app.config.from_object(DevConfig)
import models

from Person.PersonAPI import personBp
from Admin.AdminAPI import adminBp
from Notification.NotificationTypeAPI import nBp
app.register_blueprint(personBp)
app.register_blueprint(adminBp)
app.register_blueprint(nBp)

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the notification service API. There is no"
                               " resource at this endpoint."})

if __name__ == '__main__':
    models.db.init_app(app)
    app.run(port=8080)
