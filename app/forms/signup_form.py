from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

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
        validators=[DataRequired(message="Họ và chữ đệm chưa nhập")],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: Trương Hữu",
        },
    )
    first_name = StringField(
        "Tên",
        validators=[DataRequired(message="Chưa nhập tên")],
        render_kw={
            "autofocus": True,
            "autocomplete": True,
            "placeholder": "vd: Học",
        },
    )
    email = StringField(
        "Email",
        validators=[Email(message="Email chưa hợp lệ")],
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
            DataRequired("Thiếu định danh"),
            Length(min=5, message="Định danh từ 5 ký tự"),
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
            DataRequired("Cần nhập mật khẩu"),
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
    recaptcha = RecaptchaField()
    submit = SubmitField("Đăng ký")