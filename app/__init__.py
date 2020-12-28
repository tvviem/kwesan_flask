from flask import Flask
from .admin.routes import admin
from .api.routes import api
from .website.routes import website
from extensions import *
from config import config


def create_app(config_name):
    # app = Flask(__name__)
    app = Flask(__name__, static_url_path="/static")

    app.config.from_object(config[config_name])
    # Initialise extensions
    # mongo.init_app(app)
    with app.app_context():
        app.register_blueprint(admin, url_prefix="/admin")
        app.register_blueprint(api, url_prefix="/api")
        app.register_blueprint(website)
    return app