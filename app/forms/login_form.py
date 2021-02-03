from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    user_name = StringField(
        "Định danh",
        validators=[
            InputRequired("Thiếu định danh"),
            Length(min=5, message="Định danh từ 5 ký tự"),
        ],
        render_kw={
            "autofocus": True,
            "placeholder": "Tên đăng nhập"
        },
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            InputRequired("Cần nhập mật khẩu"),
        ],
        render_kw={
            "autofocus": True,
            "placeholder": "Mật khẩu"
        },
    )
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Hãy xác nhận bạn ko là robot")]
    )