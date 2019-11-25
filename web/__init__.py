from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager, AnonymousUserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Settings

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Settings)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

from web.profile.routes import profile
from web.home.routes import home
from web.auth.routes import auth

from api.auth import auth_api

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(auth_api)
