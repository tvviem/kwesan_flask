# Send an email to activate users' account
from itsdangerous import (
    URLSafeTimedSerializer,
    SignatureExpired,
    BadTimeSignature,
    BadSignature,
)

from flask import current_app as app, flash, redirect, url_for, render_template
from extensions import mail
from flask_mail import Message


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config.get("SECRET_KEY"))
    return serializer.dumps(email, salt=app.config.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config.get("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except SignatureExpired:
        # flash("Thẻ bài quá hạn, nhập email để nhận thư kích hoạt lại!", "warning")
        # return redirect(url_for("user.resend_email_confirm")) # cannot return duoc
        return 0
    except BadTimeSignature:
        return 1
    return email


def send_email(subject, to, template):
    try:
        msg = Message(subject=subject, recipients=[to], html=template)
        mail.send(msg)
    except Exception as e:
        print("Loi gui email: ", e)
