from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .forms.signup_form import RegisterForm, MAJOR_CHOICES
from .models import User, RoleType
from extensions import db

# alias user use in template with href="{{ url_for('user.<method_name>') }}"
userPage = Blueprint("user", __name__, template_folder="templates")
indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    return render_template("index.html", hasNavbar=True)


@userPage.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", hasNavbar=False)


@userPage.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    session.pop("_flashes", None)  # Clear flash message when GET signup form

    if register_form.validate_on_submit() and request.method == "POST":
        newUser = User(
            register_form.first_name.data,
            register_form.last_name.data,
            register_form.user_name.data,
            register_form.email.data,
            register_form.password.data,
            dict(MAJOR_CHOICES).get(register_form.major.data),
            register_form.about_user.data,
            RoleType.STUD,
        )
        db.session.add(newUser)
        db.session.commit()
        # Send email to user
        flash("Người dùng đã được tạo, bạn hãy xác nhận qua email", "info")
        return redirect(url_for("user.login"))
    # else:
    #     flash("Chưa tạo được người dùng", "danger")
    return render_template("signup.html", hasNavbar=False, form=register_form)
