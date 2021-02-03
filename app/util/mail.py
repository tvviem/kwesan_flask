# Send an email to activate users' account
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

from flask import current_app as app, flash, redirect, url_for
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
    except BadTimeSignature:
        flash("Đường dẫn kích hoạt không hợp lệ", "danger")
        return redirect(url_for("index.index"))
    except SignatureExpired:
        flash(
            "Đã quá thời hạn kích hoạt. Hãy nhập email để được kích hoạt lại!", "warning"
        )
        return redirect(url_for("user.resend_email_confirm"))
    return email


def send_email(subject, to, template):
    try:
        msg = Message(subject=subject, recipients=[to], html=template)
        mail.send(msg)
    except Exception as e:
        print("Loi gui email: ", e)
