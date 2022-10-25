from flask import Flask, url_for, render_template, redirect, flash, jsonify, request

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import UserRegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.get('/')
def show_home_page():
  """Show the home page and redirect to /register."""

  return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def user_register():
  """Show the user register form."""

  form = UserRegisterForm()

  if form.validate_on_submit():

    username = form.username.data
    password = form.password.data
    email = form.email.data
    firstname = form.firstname.data
    lastname = form.lastname.data

    user = User(
      username=username, 
      password=password, 
      email=email, 
      firstname=firstname, 
      lastname=lastname
    )

    db.session.add(user)
    db.session.commit()

    # do stuff with data/insert to db
    flash(f"Added {name} at {price}")
    return redirect('/secret')
    
  else:
    return render_template("user_register_form.html", form=form)

  

