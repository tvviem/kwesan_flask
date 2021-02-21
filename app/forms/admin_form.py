from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    InputRequired,
    Regexp,
)

# class ManageUsersForm(FlaskForm):
