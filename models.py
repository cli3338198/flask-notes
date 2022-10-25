from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True,
        nullable=False,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    firstname = db.Column(
        db.String(30),
        nullable=False,

    )

    lastname = db.Column(
        db.String(30),
        nullable=False,
    )

    @classmethod
    def register(cls,
                 username,
                 password,
                 email,
                 firstname,
                 lastname
                 ):
        """Registers the user, creates a hashed password, return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username,
                   password=hashed,
                   email=email,
                   firstname=firstname,
                   lastname=lastname
                   )

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate the user, if not authenticated, return False"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        else:
            return False

class Note(db.Model):
    """Note."""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    owner = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False
    )


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
