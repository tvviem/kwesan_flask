from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    Email,
    Length,
    EqualTo,
    InputRequired,
    Regexp,
)


class ProvidingEmailForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired(message="Chưa nhập email"),
            Email(message="Email chưa hợp lệ"),
        ],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: thhoc@gmail.com",
            "title": "Hãy cung cấp email mà bạn đang dùng",
        },
    )
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Hãy xác nhận bạn ko là robot")]
    )
    submit = SubmitField("Xác nhận")


class ResetPwdForm(FlaskForm):
    email = StringField(
        label="Email",
        render_kw={
            "disabled": True,
        },
    )
    user_name = StringField(
        label="Định danh",
        render_kw={
            "disabled": True,
        },
    )
    password = PasswordField(
        label="Mật khẩu",
        validators=[
            InputRequired("Cần nhập mật khẩu"),
            Length(min=8, message="Mật khẩu ít nhất 8 ký tự"),
            EqualTo("confirm_pass", message="Nhập lại mật khẩu chưa chính xác"),
        ],
        render_kw={
            "autofocus": True,
            "placeholder": "mật khẩu từ 8 ký tự",
        },
    )
    confirm_pass = PasswordField(
        label="Nhập lại mật khẩu",
        render_kw={
            "autofocus": True,
            "placeholder": "Xác nhận mật khẩu",
            "required": True,
        },
    )
