from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    InputRequired,
    ValidationError,
    Regexp,
)

MAJOR_CHOICES = [
    ("1", "Công nghệ thông tin"),
    ("2", "Ngôn ngữ Anh"),
    ("3", "Quản trị kinh doanh"),
    ("4", "Sư phạm"),
    ("5", "Khác"),
]


class RegisterForm(FlaskForm):
    last_name = StringField(
        "Họ và chữ đệm",
        validators=[InputRequired(message="Họ và chữ đệm chưa nhập")],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: Trương Hữu",
        },
    )
    first_name = StringField(
        "Tên",
        validators=[InputRequired(message="Chưa nhập tên")],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: Học",
        },
    )
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
    user_name = StringField(
        "Định danh",
        validators=[
            InputRequired("Thiếu định danh"),
            Length(min=5, max=25, message="Định danh từ 5 ký tự"),
            Regexp("^[a-zA-Z]\w+$", message="Định danh bắt đầu từ ký tự chữ"),
        ],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: thhoc",
            "title": "Bắt đầu là ký tự chữ, không chứa khoảng trắng",
        },
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            InputRequired("Cần nhập mật khẩu"),
            Length(min=8, message="Mật khẩu ít nhất 8 ký tự"),
            EqualTo("confirm_pass", message="Nhập lại mật khẩu chưa chính xác"),
        ],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "mật khẩu từ 8 ký tự",
        },
    )
    confirm_pass = PasswordField(
        "Nhập lại mật khẩu",
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "Xác nhận mật khẩu",
        },
    )
    major = SelectField("Ngành học", choices=MAJOR_CHOICES)
    about_user = TextAreaField(
        "Tóm tắt bản thân",
        render_kw={
            "rows": "3",
            "placeholder": "Sinh viên năm mấy? Khoa, trường học?",
        },
    )
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Hãy xác nhận bạn ko là robot")]
    )
    submit = SubmitField("Đăng ký")
