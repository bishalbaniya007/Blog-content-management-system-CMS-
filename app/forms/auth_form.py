from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from sqlalchemy import select
from app.extensions import db
from app.models import User

# form for registration
class RegistrationForm(FlaskForm):
  username = StringField(
    "Username",
    validators=[DataRequired(),
                Regexp(r'^[a-zA-Z0-9_-]{3,16}$', 
                       message="Username must be of 3 to 16 char and contain only letters, numbers, hyphens, or underscores.")]
  )

  email = StringField(
    "Email",
    validators=[DataRequired(),
                 Email(),
                 Length(max=50)]
  )

  password = PasswordField(
    "Password",
    validators=[DataRequired(),
                Length(min=8, message="Password length must be of at least 8 characters."),
                Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$',
                       message="Password must contain  at least 1 lowercase, 1 uppercase, 1 number, and 1 special character.")]
  )

  confirm = PasswordField(
    "Confirm Password",
    validators=[DataRequired(),
                EqualTo('password',
                  message="Password do not match.")]
  )

  submit = SubmitField("Register")    # this creates a html submit button


  # custom validators
  def validate_username(self, field):
    if db.session.scalar(select(User).where(User.username == field.data)):
      raise ValidationError("Username is already taken.")


  def validate_email(self, field):
    if db.session.scalar(select(User).where(User.email == field.data.lower())):
      raise ValidationError("Email is already registered.")


# form for login
class LoginForm(FlaskForm):
  email = StringField(
    "Email",
    validators=[DataRequired(),
                Email()]
  )

  password = PasswordField(
    "Password",
    validators=[DataRequired()]
  )

  submit = SubmitField("Login")
  
