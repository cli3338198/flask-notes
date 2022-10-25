from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

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

      hashed = Bcrypt.generate_password_hash(f'{username} {password}').decode('utf8')

      return cls(username=username, 
        password=hashed, 
        email=email, 
        firstname=firstname, 
        lastname=lastname
      )

  @classmethod
  def authenticate(cls, username, password):
    """Authenticate the user."""

    user = cls.query.get_or_404(username).one_or_none()

    if user and Bcrypt.check_password_hash(f'{username} {password}', user.password):
      return user

    else:
      return False



def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)