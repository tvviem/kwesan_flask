from flask import Flask, url_for

from .admin.routes import admin
from .lecturer.routes import lecturer
from .api.routes import api
from .student.routes import studentPage
from config import config
from .routes import userPage, indexPage
from extensions import db, bcrypt


def create_app(config_name):
    # app = Flask(__name__)
    # static_url_path set for showing client, static_folder for server directory
    app = Flask(__name__, static_url_path="/public", static_folder="static")
    app.config.from_object(config[config_name])
    # assets = Environment(app)
    # assets.debug = True
    # assets.register(bundles)

    # Initialise from extensions
    db.init_app(app)
    bcrypt.init_app(app)
    # mongo.init_app(app)
    # print(app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()  # for create all tables with database existed
        app.register_blueprint(admin, url_prefix="/admin")
        app.register_blueprint(lecturer, url_prefix="/lecturer")
        app.register_blueprint(studentPage, url_prefix="/student")
        app.register_blueprint(userPage, url_prefix="/user")
        app.register_blueprint(indexPage)
        app.register_blueprint(api, url_prefix="/api")

    return app


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("/user/login"))

    return wrap