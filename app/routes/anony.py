from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)
from ..forms.signup_form import RegisterForm, MAJOR_CHOICES
from ..forms.login_form import LoginForm
from ..models import User, RoleType
from extensions import db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from ..util.mail import generate_confirmation_token, confirm_token, send_email
from ..util.query import UserQuery
from datetime import datetime
import re  # support valid string with regular expressions

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
        if isinstance(user, User) and user.verify_password(form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember.data)
                if user.role == RoleType.ADMI:
                    return redirect(url_for("admin.home"))
                elif user.role == RoleType.LECT:
                    return redirect(url_for("lecturer.home"))
                elif user.role == RoleType.STUD:
                    return redirect(url_for("student.home"))
                else:
                    return abort(403)
            else:
                flash("Tài khoản chưa xác nhận qua email", "warning")
                return render_template("login.html", form=form)
        else:
            flash("Thông tin tài khoản chưa đúng", "warning")
            return render_template("login.html", form=form)
    return render_template("login.html", hasNavbar=False, form=form)


@userPage.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    # session.pop("_flashes", None)  # Clear flash message when GET signup form
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
        content = "Xin chào, bạn vừa tạo tài khoản. Hãy sử dụng đường dẫn bên dưới để kích hoạt tài khoản!"
        html = render_template("activate.html", confirm_url=confirm_url, content=content)
        subject = "Please confirm email with Kwesan-Sys!"
        send_email(subject, newUser.email, html)

        # mark user with signed in status
        # login_user(newUser)

        flash("Người dùng đã được tạo, bạn hãy xác nhận qua email", "info")
        return redirect(url_for("index.index"))
    return render_template("signup.html", hasNavbar=False, form=register_form)


@userPage.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if email == 0:
        flash("Thẻ bài quá hạn, nhập email để nhận thư kích hoạt lại!", "warning")
        return redirect(url_for("user.resend_email_confirm", hasNavbar=True))
    if email == 1:
        flash("Thẻ kích hoạt không hợp lệ, hãy đăng ký tài khoản!", "danger")
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
        # replace {2,3} by + for custom email
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.search(regex, request.form.get("email")):
            flash("Email không hợp lệ!", "warning")
            return render_template("reactive.html", hasNavbar=True)
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user is None:
            flash("Email chưa được sử dụng!", "info")
            return render_template("reactivate.html")
        else:
            if not user.confirmed:
                token = generate_confirmation_token(user.email)
                confirm_url = url_for("user.confirm_email", token=token, _external=True)
                content = "Chào bạn, thẻ kích hoạt của bạn có thể quá hạn. Sử dụng link sau để kích hoạt lại."
                html = render_template(
                    "activate.html", confirm_url=confirm_url, content=content
                )
                subject = "Again! Please confirm email with Kwesan-Sys"
                send_email(subject, user.email, html)
                flash("Đã gửi lại email kích hoạt!", "success")
                return redirect(url_for("index.index"))
            else:
                flash("Tài khoản đã kích hoạt trước đó, hãy đăng nhập!", "success")
                return redirect(url_for("user.login"))
    else:
        return render_template("reactivate.html")


@userPage.route("/resetpwd/<token>")
def reset_pwd_via_email(token):
    email = confirm_token(token)
    if email == 0:
        flash("Thẻ bài quá hạn, nhập email để nhận thiệt lập mật khẩu!", "warning")
        return redirect(url_for("user.forget_password", hasNavbar=True))
    if email == 1:
        flash("Thẻ kích hoạt không hợp lệ, hãy đăng ký tài khoản!", "danger")
        return redirect(url_for("index.index"))
    user = User.query.filter_by(email=email).first_or_404()
    if not user.confirmed:
        # Kich hoat tai khoan neu chua confirmed, va gui link reset pwd
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
    return render_template("reset_password_fields.html", hasNavbar=True, email=email)


@userPage.route("/forget-password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        # replace {2,3} by + for custom email
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.search(regex, request.form.get("email")):
            flash("Email không hợp lệ!", "warning")
            return render_template("reset_password.html", hasNavbar=True)
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user is None:
            flash("Email chưa được sử dụng!", "info")
        else:
            # Send email to user to reset password
            token = generate_confirmation_token(user.email)
            confirm_url = url_for("user.reset_pwd_via_email", token=token, _external=True)
            content = "Xin chào, bạn đã quên mật khẩu. Hãy sử dụng đường dẫn bên dưới để thiết lập lại mật khẩu!"
            html = render_template(
                "activate.html", confirm_url=confirm_url, content=content
            )
            subject = "Please reset your password with below link!"
            send_email(subject, user.email, html)
            flash("Đã gửi email reset tài khoản!", "info")
            return redirect(url_for("index.index"))

    return render_template("reset_password.html", hasNavbar=True)


@userPage.route("/reset-password", methods=["GET", "POST"])
def reset_pwd_with_form():
    if request.method == "POST":
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        email = request.form.get("email")
        if not re.search(regex, email):
            flash("Email không hợp lệ!", "warning")
            return render_template(
                "reset_password_fields.html", hasNavbar=True, email=email
            )

        user = User.query.filter_by(email=email).first()
        password1 = request.form.get("password1").strip()
        password2 = request.form.get("password2").strip()
        if user is None:
            flash("Email chưa đăng ký người dùng")
            return render_template(
                "reset_password_fields.html", hasNavbar=True, email=email
            )
        if password1 == password2:
            user.set_password(password1)
        else:
            flash("Nhập mật khẩu 2 lần phải giống nhau")
            return render_template(
                "reset_password_fields.html", hasNavbar=True, email=email
            )
        db.session.add(user)
        db.session.commit()
        flash("Thay đổi mật khẩu thành công")
        return redirect(url_for("user.login"))

    abort(403)


@userPage.route("/home")
@login_required
def home():
    user = current_user
    if user.role == RoleType.ADMI:
        return redirect(url_for("admin.home"))
    elif user.role == RoleType.LECT:
        return redirect(url_for("lecturer.home"))
    elif user.role == RoleType.STUD:
        return redirect(url_for("student.home"))
    else:
        return abort(403)


@userPage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))