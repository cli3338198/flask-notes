from flask import Flask, render_template, redirect, flash, session

from models import db, connect_db, User, Note
from forms import UserRegisterForm, UserLoginForm, UserLogoutForm, UserDeleteForm, NoteAddForm
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

        user = User.register(username=username,
                             password=password,
                             email=email,
                             firstname=firstname,
                             lastname=lastname
                             )
        db.session.add(user)
        db.session.commit()

        session['username'] = username

        # do stuff with data/insert to db
        flash(f"Successfully registered {username}")
        return redirect(f'/users/{username}')

    else:
        return render_template("user_register_form.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def user_login():
    """Log the user in and validate else rerender the login form"""
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)


@app.get('/users/<username>')
def user_show_secret(username):
    """Show the user detail page if not in session redirect to '/login' """

    form = UserLogoutForm()

    notes = Note.query.filter_by(owner=username).all()

    if "username" not in session:
        return redirect('/login')
    else:
        user = User.query.get(username)
        return render_template('user_detail.html', user=user, form=form, notes=notes)

@app.post('/logout')
def user_logout():
    """Log out the user and remove from session and redirect to '/' """

    form = UserLogoutForm()

    if form.validate_on_submit():
        session.pop('username', None)

    return redirect('/')

@app.post('/users/<username>/delete')
def user_delete(username):
    """Delete the user, delete all notes, redirect to '/' """

    user = User.query.get_or_404(username)
    form = UserDeleteForm()

    if form.validate_on_submit():
        session.pop('username', None)
        notes = Note.query.filter_by(owner=username)
        #test this out
        notes.delete()

        db.session.delete(user)
        db.session.commit()
        
        return redirect('/')

    return redirect(f'/users/{username}')


################################################################################
    
@app.route('/users/<username>/notes/add', methods=["POST", "GET"])
def note_add(username):
    """Display the note add form"""

    user = User.query.get_or_404(username)
    form = NoteAddForm()

    if user and form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)

        db.session.add(note)
        db.session.commit()
        return redirect(f'/users/{username}')

    else:
        return render_template("note_add_form.html", form=form)

