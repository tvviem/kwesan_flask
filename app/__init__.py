from flask import Flask

from .admin.routes import admin
from .lecturer.routes import lecturer
from .api.routes import api
from .student.routes import studentPage
from extensions import *
from config import config
from .routes import userPage, indexPage
from flask_sqlalchemy import SQLAlchemy

# from flask_assets import Environment, Bundle
# from .util.assets import bundles
db = SQLAlchemy()


def create_app(config_name):
    # app = Flask(__name__)
    # static_url_path set for showing client, static_folder for server directory
    app = Flask(__name__, static_url_path="/public", static_folder="static")
    app.config.from_object(config[config_name])
    db.init_app(app)
    # assets = Environment(app)
    # assets.debug = True
    # assets.register(bundles)

    # Initialise extensions
    # mongo.init_app(app)
    # print(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.create_all()
        app.register_blueprint(admin, url_prefix="/admin")
        app.register_blueprint(lecturer, url_prefix="/lecturer")
        app.register_blueprint(studentPage, url_prefix="/student")
        app.register_blueprint(userPage, url_prefix="/user")
        app.register_blueprint(indexPage)
        app.register_blueprint(api, url_prefix="/api")

    return app