from app import create_app
from flask import session, render_template, send_from_directory
from os import path
from app.models import User, RoleType
from extensions import db
from datetime import datetime

app = create_app("development")

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.before_request
# def clear_flash_messages():
#     session.pop("_flashes", None)


@app.before_first_request
def create_db_default_admin_user():
    db.create_all()  # for create all tables with database existed
    db.session.commit()
    admin_exist = User.query.filter(User.id == 1, User.role == RoleType.ADMI).first()
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


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html", title="Unauthorized_403"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", title="Not_found_404"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html", title="Internal_server_error"), 500


if __name__ == "__main__":
    app.run(debug=True)


"""
@app.route("/user", methods=["GET"])
def user_records():
    username = request.args.get("user")
    email = request.args.get("email")
    print(username, email)
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(f"{username} ({email}) already created!")
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False,
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for("login"))
    return render_template("user.login", users=User.query.all(), title="Show Users")
 """
