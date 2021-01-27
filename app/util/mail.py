# Send an email to activate users' account
from itsdangerous import URLSafeTimedSerializer

from flask import current_app as app
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
    except:
        return False
    return email


def send_email(subject, to, template):
    try:
        msg = Message(subject=subject, recipients=[to], html=template)
        mail.send(msg)
        # print(
        #     "EMAIL:",
        #     app.config.get("MAIL_USERNAME"),
        #     app.config.get("MAIL_PASSWORD"),
        #     app.config.get("MAIL_USE_SSL"),
        # )
    except Exception as e:
        print(
            "Loi gui email: ",
            e,
            "SSL: ",
            app.config.get("MAIL_USE_SSL"),
            "TLS: ",
            app.config.get("MAIL_USE_TLS"),
            app.config.get("MAIL_PORT"),
        )
