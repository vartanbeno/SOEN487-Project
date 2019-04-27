from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_sqlalchemy import SQLAlchemy

from messaging_service.helpers.response import response

db = SQLAlchemy()
jwt = JWTManager()

url_prefix = '/api'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, resources={fr'{url_prefix}/*': {'origins': '*'}})

    db.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return response('Page not found.', 404)

    from messaging_service.routes.conversation import conversation_api
    from messaging_service.routes.message import message_api

    app.register_blueprint(conversation_api, url_prefix=f'{url_prefix}/conversation')
    app.register_blueprint(message_api, url_prefix=f'{url_prefix}/message')

    return app
