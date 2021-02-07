from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..forms.signup_form import RegisterForm, MAJOR_CHOICES
from ..forms.login_form import LoginForm
from ..models import User, RoleType
from extensions import db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from ..util.mail import generate_confirmation_token, confirm_token, send_email
from ..util.query import UserQuery
from datetime import datetime

# alias user use in template with href="{{ url_for('user.<method_name_for_route>') }}"
userPage = Blueprint("user", __name__, template_folder="templates")
indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    # user = current_user
    # if user: # neu nguoi dung da dang nhap chuyen den trang home tuong ung quyen
    #     print("User is_authenticated()")
    # else:
    #     print("User NOT is_authenticated()")
    return render_template("index.html", hasNavbar=True)


@userPage.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.user_name.data).first()
        if isinstance(user, User) and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            # flash("Welcome.", "success")
            if user.role == RoleType.ADMI:
                return redirect(url_for("admin.home"))
            elif user.role == RoleType.LECT:
                return redirect(url_for("lecturer.home"))
            else:
                return redirect(url_for("student.home"))
        else:
            flash("Thông tin tài khoản chưa đúng", "warning")
            return render_template("login.html", form=form)

    return render_template("login.html", hasNavbar=False, form=form)


@userPage.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    session.pop("_flashes", None)  # Clear flash message when GET signup form
    if register_form.validate_on_submit() and request.method == "POST":
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

        # Send email to user
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
    session.pop("_flashes", None)

    email = confirm_token(token)
    if email == 0:
        flash("Thẻ bài quá hạn, nhập email để nhận thư kích hoạt lại!", "warning")
        return redirect(url_for("user.resend_email_confirm", hasNavbar=True))
    if email == 1:
        # flash("Thẻ kích hoạt không hợp lệ, hãy tạo tài khoản!", "danger")
        return redirect(url_for("index.index"))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Tài khoản đã kích hoạt trước đó, hãy đăng nhập!", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("Kích hoạt tài khoản thành công, hãy đăng nhập!", "success")
    return redirect(url_for("user.login"))


@userPage.route("/resend", methods=["GET", "POST"])
def resend_email_confirm():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first_or_404()
        if not user.confirmed:
            if isinstance(user, User):  # or use: user is not None
                token = generate_confirmation_token(user.email)
                confirm_url = url_for("user.confirm_email", token=token, _external=True)
                html = render_template("activate.html", confirm_url=confirm_url)
                subject = "Again! Please confirm email with Kwesan-Sys"
                send_email(subject, user.email, html)
                flash("Đã gửi lại email kích hoạt!", "success")
                return redirect(url_for("index.index"))
            else:
                flash("Email chưa được sử dụng. Hãy đăng ký với mẫu sau!", "info")
                return redirect(url_for("user.register"))
        else:
            flash("Tài khoản đã kích hoạt trước đó, hãy đăng nhập!", "success")
            return redirect(url_for("user.login"))
    else:
        return render_template("reactivate.html")


@userPage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))