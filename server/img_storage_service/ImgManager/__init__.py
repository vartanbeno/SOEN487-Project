import datetime
from flask import Flask
from ImgManager.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_simple import JWTManager


# need an app before we import models because models need it
app = Flask(__name__)
app.config['SECRET_KEY'] = 'teamgiovanniprattico'
app.config['JWT_SECRET_KEY'] = 'teamgiovanniprattico'
app.config['JWT_EXPIRES'] = datetime.timedelta(days=1)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from ImgManager import routes
