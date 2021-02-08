from flask import Flask, url_for

from .routes.admin import adminRoutes
from .routes.lecturer import lecturerRoutes
from .routes.student import studentRoutes
from .api.routes import api
from config import config
from .routes.anony import userPage, indexPage
from extensions import db, bcrypt, login_manager, mail
from .models import User


def create_app(config_name):
    # static_url_path set for showing client, static_folder for server directory
    app = Flask(__name__, static_url_path="/public", static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # assets = Environment(app)
    # assets.debug = True
    # assets.register(bundles)

    # Initialise from extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # print(app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        app.register_blueprint(indexPage)
        app.register_blueprint(userPage, url_prefix="/user/")
        app.register_blueprint(adminRoutes, url_prefix="/admin/")
        app.register_blueprint(lecturerRoutes, url_prefix="/lecturer/")
        app.register_blueprint(studentRoutes, url_prefix="/student/")
        app.register_blueprint(api, url_prefix="/api/")
        login_manager.login_view = url_for(
            "user.login"
        )  # have to set SERVER_NAME in .env

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))