from app import create_app

from flask import request, render_template, make_response, url_for, redirect
from datetime import datetime as dt
from app import db
from app.models import User

# from flask import current_app as app
app = create_app("development")


@app.route("/user", methods=["GET"])
def user_records():
    """Create a user via query string parameters."""
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


if __name__ == "__main__":
    # print(app.config.get("SECRET_KEY"))
    app.run(debug=True)
