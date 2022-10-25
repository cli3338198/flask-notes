from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class UserRegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(max=100)])

    email = StringField(
        'Email',
        validators=[InputRequired(), Length(max=50)])

    firstname = StringField(
        'First Name',
        validators=[InputRequired(), Length(max=30)])

    lastname = StringField(
        'Last Name',
        validators=[InputRequired(), Length(max=30)])


class UserLoginForm(FlaskForm):
    """ Form for logging user in"""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(max=100)])


class UserLogoutForm(FlaskForm):
    """ Form for logging user out"""

class UserDeleteForm(FlaskForm):
    """Form for deleting a user."""

class NoteAddForm(FlaskForm):
    """Form for adding a note"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])

    content = StringField("Content", validators=[InputRequired()])
