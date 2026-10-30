from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
  title = StringField(
    "Title",
    validators=[DataRequired(),
                Length(max=100)]
  )

  body = TextAreaField(
    "Body",
    validators=[DataRequired()]
  )

  status = SelectField(
    "Status",
    choices=[("draft", "Draft"),
             ("published", "Published")]
  )

  submit = SubmitField("Save")

