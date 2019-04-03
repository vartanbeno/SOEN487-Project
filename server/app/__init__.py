from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.helpers.response import response

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

url_prefix = '/api'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, resources={fr'{url_prefix}/*': {'origins': '*'}})

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return response('Page not found.', 404)

    # todo register blueprints

    return app
