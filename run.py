from app import create_app
from flask import session, render_template, send_from_directory, url_for
from os import path
from app.models import User, RoleType
from extensions import db, login_manager
from datetime import datetime, timedelta

app = create_app("development")

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# NOTICE: REVIEW it
@app.before_request
def make_session_permanent():
    # Trong khoang thoi gian M phut
    # neu nguoi dung ko co tuong tac (REQUEST) thi SE TU DONG LOGOUT
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.before_first_request
def create_db_default_admin_user():
    admin_exist = User.query.filter((User.id == 1) | (User.role == RoleType.ADMI)).first()
    if admin_exist is None:
        db.session.add(
            User(
                firstname="Viem",
                lastname="Trieu Vinh",
                username="tvviem",
                email="bluitdev@gmail.com",
                password="tvviem123",
                major="it-admin",
                aboutuser="Ham muốn làm ra ứng dụng",
                role=RoleType.ADMI,
                confirmed=True,
                confirmed_on=datetime.now(),
            )
        )
        db.session.commit()
    login_manager.login_view = url_for("user.login")


# @app.after_request
# def add_security_headers(resp):
#     resp.set_cookie("appname", "kwesys", httponly=True, samesite="Lax")
#     # resp.headers["Content-Security-Policy"] = "default-src 'self'"
#     return resp


if __name__ == "__main__":
    # app.run(threaded=True)
    app.run()