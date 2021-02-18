""" we will be initializing our Flask extensions for use in our blueprints. """
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.util import sse

# from flask_assets import Environment, Bundle
# from .util.assets import bundles

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

announcer = sse.MessageAnnouncer()