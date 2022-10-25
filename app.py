from flask import Flask, url_for, render_template, redirect, flash, jsonify, request, session

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import UserRegisterForm, UserLogin
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


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

        user = User.register(username=username,
                             password=password,
                             email=email,
                             firstname=firstname,
                             lastname=lastname
                             )
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        # do stuff with data/insert to db
        flash(f"Successfully registered {username}")
        return redirect('/secret')

    else:
        return render_template("user_register_form.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def user_login():

    form = UserLogin()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)


@app.get('/users/<username>')
def user_show_secret(username):
    if 'username' not in session:
        return redirect('/login')
    else:
        user = User.query.get(username)
        return render_template('user_detail.html', user=user)
