from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_mail import Mail
from flask import Flask


from settings import Settings

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Settings)

login_manager = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
api = Api(app)

from web.profile.routes import profile
from web.home.routes import home
from web.auth.routes import auth

from api.auth import api_auth
from api.users import api_users

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(api_auth)
app.register_blueprint(api_users)
