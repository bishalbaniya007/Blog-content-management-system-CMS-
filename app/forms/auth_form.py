from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from sqlalchemy import select
from app.extensions import db
from app.models import User

# form for registration
class RegisterForm(FlaskForm):
  username = StringField(
    "Username",
    validators=[DataRequired(),
                Regexp(r'^[a-zA-Z0-9_-]{3,16}$', 
                       message="Username must contain only letters, numbers, hyphens, or underscores.")]
  )

  email = StringField(
    "Email",
    Validatiors=[DataRequired(),
                 Email(),
                 Length(max=50)]
  )

  password = PasswordField(
    "Password",
    validators=[DataRequired(),
                Length(min=8, message="Password lenght must be of at least 8 characters."),
                Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                       message="Password must contain  at least 1 lowercase, 1 uppercase, 1 number, and 1 special char.")]
  )

  confirm = PasswordField(
    "Confirm Password",
    validators=[DataRequired(),
                EqualTo('confirm',
                  message="Password do not match.")]
  )

  submit = SubmitField("Register")    # this creates a html submit button


  # custom validators
  def validate_username(self, field):
    if db.session.scalar(select(User).where(User.username == field.data)):
      raise ValidationError("Username is already taken.")


  def validate_email(self, field):
    if db.session.scalar(select(User).where(User.email == field.data)):
      raise ValidationError("Email is already registered.")


# form for login
class LoginFrom(FlaskForm):
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
  
