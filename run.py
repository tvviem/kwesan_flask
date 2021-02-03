from app import create_app
from flask import render_template
# from flask import current_app as app

app = create_app("development")
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


