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
        'Email',  # there is a better validator - email
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


class CSRFForm(FlaskForm):
    """ Form for validating CSRF token"""


class NoteAddForm(FlaskForm):
    """Form for adding a note"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])

    content = StringField("Content", validators=[InputRequired()])


class NoteEditForm(FlaskForm):
    """ Form for editing note """

    title = StringField("Title", validators=[
        InputRequired(), Length(max=100)])

    # textarea in wtform to make text box larger
    content = StringField("Content", validators=[InputRequired()])
