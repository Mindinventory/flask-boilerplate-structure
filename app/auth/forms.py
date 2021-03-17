from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# Define the User Signup form (WTForms)
class SignupForm(FlaskForm):
    first_name = StringField(validators=[DataRequired(), Length(min=2)],
                             description='First Name')

    last_name = StringField(validators=[DataRequired(), Length(min=2)],
                            description='Last Name')

    email = EmailField(validators=[DataRequired(), Email()],
                       description='Email address')

    password = PasswordField(validators=[
        DataRequired(), Length(min=8),
        EqualTo('confirm', message='Passwords must match.')
    ], description='Password')

    confirm = PasswordField(description='Confirm password')


# Define the User Login form (WTForms)
class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()],
                       description='Email address')

    password = PasswordField(validators=[DataRequired()],
                             description='Password')


# Define the User forgot password form (WTForms)
class ForgotForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],
                        description='Email address')


# Define the User reset password form (WTForms)
class ResetForm(FlaskForm):
    password = PasswordField(validators=[
        DataRequired(), Length(min=8),
        EqualTo('confirm', message='Passwords must match.')
    ], description='Password')

    confirm = PasswordField(description='Confirm password')
