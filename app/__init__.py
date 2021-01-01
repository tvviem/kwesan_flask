from flask import Flask
from flask_assets import Environment, Bundle
from .admin.routes import admin
from .lecturer.routes import lecturer
from .api.routes import api
from .student.routes import studentPage
from extensions import *
from config import config
from .routes import loginPage, indexPage

# from .util.assets import bundles


def create_app(config_name):
    # app = Flask(__name__)
    # static_url_path set for showing client, static_folder for server directory
    app = Flask(__name__, static_url_path="/public", static_folder="static")
    app.config.from_object(config[config_name])
    # assets = Environment(app)
    # assets.debug = True
    # assets.register(bundles)

    # Initialise extensions
    # mongo.init_app(app)
    with app.app_context():
        app.register_blueprint(admin, url_prefix="/admin")
        app.register_blueprint(lecturer, url_prefix="/lecturer")
        app.register_blueprint(studentPage, url_prefix="/student")
        app.register_blueprint(loginPage)
        app.register_blueprint(indexPage)
        app.register_blueprint(api, url_prefix="/api")
    return app