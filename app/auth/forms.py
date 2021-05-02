from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


# For each field, an object is created as a class variable
# in the LoginForm class. Each field is given a description or label as a first argument.
class LoginForm(FlaskForm):
    login_username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    login_password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember me')
    login_submit = SubmitField('LOGIN', render_kw={"class": "submit"})


class RegistrationForm(FlaskForm):
    register_username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    register_password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    register_password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm "
                                                                                                       "Password"})
    registration_submit = SubmitField('SIGN UP', render_kw={"class": "submit"})

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def validate_email( email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')