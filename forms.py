"""Forms for Flask Feedback."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegisterUserForm(FlaskForm):
    """Form for registering users."""

    username = StringField("Username", validators=[DataRequired(),Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired(),Length(max=50)])
    first_name = StringField("First Name", validators=[DataRequired(),Length(max=30)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(max=30)])

class LoginUserForm(FlaskForm):
    """Form for logging in users."""

    username = StringField("Username", validators=[DataRequired(),Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    
class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title", validators=[DataRequired(),Length(max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
