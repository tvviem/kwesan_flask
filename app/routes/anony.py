from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..forms.signup_form import RegisterForm, MAJOR_CHOICES
from ..forms.login_form import LoginForm
from ..models import User, RoleType
from extensions import db
from flask_login import login_required, login_user
from ..util.mail import generate_confirmation_token, confirm_token, send_email
from ..util.query import UserQuery
from datetime import datetime

# alias user use in template with href="{{ url_for('user.<method_name_for_route>') }}"
userPage = Blueprint("user", __name__, template_folder="templates")
indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    return render_template("index.html", hasNavbar=True)


@userPage.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('admin.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)

    return render_template("login.html", hasNavbar=False, form=form)


@userPage.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    session.pop("_flashes", None)  # Clear flash message when GET signup form
    if register_form.validate_on_submit() and request.method == "POST":
        # foundUser = User.query.filter_by(or_(email=register_form.email.data, username=register_form.user_name.data)).first()
        # if UserQuery.get_user_id_by_email_or_username(register_form.email.data, register_form.user_name.data) is not None:
        #     flash("Email và username đã đăng ký, hãy chọn email/username khác!", "danger")
        #     return render_template("signup.html", hasNavbar=False, form=register_form)

        if UserQuery.is_existing_email(register_form.email.data):
            flash("Email đã đăng ký, hãy chọn email khác!", "danger")
            return render_template("signup.html", hasNavbar=False, form=register_form)

        if UserQuery.is_existing_username(register_form.user_name.data):
            flash("Định danh đã dùng, hãy chọn định danh khác!", "danger")
            return render_template("signup.html", hasNavbar=False, form=register_form)

        newUser = User(
            register_form.first_name.data,
            register_form.last_name.data,
            register_form.user_name.data,
            register_form.email.data,
            register_form.password.data,
            dict(MAJOR_CHOICES).get(register_form.major.data),
            register_form.about_user.data,
            RoleType.STUD,
            confirmed=False,
        )
        db.session.add(newUser)
        db.session.commit()
        token = generate_confirmation_token(newUser.email)
        confirm_url = url_for("user.confirm_email", token=token, _external=True)
        html = render_template("activate.html", confirm_url=confirm_url)

        subject = "Please confirm email with Kwesan-Sys!"
        send_email(subject, newUser.email, html)
        # mark user with signed in status
        # login_user(newUser)

        flash("Người dùng đã được tạo, bạn hãy xác nhận qua email", "info")
        return redirect(url_for("index.index"))
    # else:
    #     flash("Chưa tạo được người dùng", "danger")
    return render_template("signup.html", hasNavbar=False, form=register_form)


@userPage.route("/confirm/<token>")
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("index.index"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("user.login"))
