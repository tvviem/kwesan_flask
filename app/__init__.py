from flask import Flask, url_for, render_template

from .routes.admin import adminRoutes
from .routes.lecturer import lecturerRoutes
from .routes.student import studentRoutes
from .api.routes import api
from config import config
from .routes.anony import userPage, indexPage
from extensions import db, bcrypt, login_manager, mail
from .models import User


def init_logging(curApp):
    for handler in curApp.logger.handlers:
        curApp.logger.removeHandler(handler)

    # logging.basicConfig(filename='kwesansys.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    import os, logging
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'kwesansys.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    from logging import Formatter
    handler.setFormatter(Formatter(f'%(asctime)s %(levelname)s %(name)s : %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    curApp.logger.addHandler(handler)

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

    init_logging(curApp=app)

    # print(app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()
        app.register_blueprint(indexPage)
        app.register_blueprint(userPage, url_prefix="/user/")
        app.register_blueprint(adminRoutes, url_prefix="/admin/")
        app.register_blueprint(lecturerRoutes, url_prefix="/lecturer/")
        app.register_blueprint(studentRoutes, url_prefix="/student/")
        app.register_blueprint(api, url_prefix="/api/")
        # app.register_error_handler(401, unauthorized_page)
        app.register_error_handler(403, forbidden_page)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(405, method_not_allowed)
        app.register_error_handler(500, server_error_page)

    return app


# def unauthorized_page(error):
#     return render_template("errors/401.html", title="Unauthorized_401"), 401


# @app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html", title="Forbidden_403"), 403


# @app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", title="Not_found_404"), 404


# @app.errorhandler(405)
def method_not_allowed(error):
    return render_template("errors/405.html", title="Method_not_allowed_405"), 405


# @app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html", title="Internal_server_error_500"), 500


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    from flask import flash, redirect

    flash("Cần đăng nhập để truy xuất", "warning")
    return redirect(url_for("user.login"))
