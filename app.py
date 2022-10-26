from flask import Flask, render_template, redirect, flash, session

from models import db, connect_db, User, Note
from forms import CSRFForm, UserRegisterForm, UserLoginForm, NoteAddForm, NoteEditForm
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_home_page():
    """Show the homepage and redirect to /register."""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def user_register():
    """Show the user register form.
    If input is valid, redirect to user profile page.
    If input is invalid, return user to registration form."""

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
    """Log the user in.
    If form input is valid, redirect to user profile page.
    If password/username is not authenticated, display error.
    If form input is invalid, redirect to the login form"""

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = username
            flash(f"Successfully logged in!")
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)


@app.get('/users/<username>')
def user_show_secret(username):
    """Show the user detail page if user is logged in.
    If not in session, redirect to login page """

    if "username" not in session:  # best to keep this at the top of function to act as guard
        return redirect('/login')

    form = CSRFForm()

    notes = Note.query.filter_by(owner=username).all()  # create backref

    user = User.query.get(username)
    return render_template('user_detail.html', user=user, form=form, notes=notes)


@app.post('/logout')
def user_logout():
    """Log out the user and remove from session. Redirect to homepage """

    form = CSRFForm()

    if form.validate_on_submit():
        session.pop('username', None)

    flash(f"Successfully logged out!")
    return redirect('/')


@app.post('/users/<username>/delete')
def user_delete(username):
    """Delete the user and all notes related to the user.
    If form input is valid, redirect to homepage.
    If form input is invalid, redirect to user detail page"""

    user = User.query.get_or_404(username)
    form = CSRFForm()

    if form.validate_on_submit():
        session.pop('username', None)
        notes = Note.query.filter_by(owner=username)
        # test this out
        notes.delete()

        db.session.delete(user)
        db.session.commit()

        flash(f"{username} has been deleted!")
        return redirect('/')

    return redirect(f'/users/{username}')


################################################################################

@app.route('/users/<username>/notes/add', methods=["POST", "GET"])
def note_add(username):
    """Display the note add form.
    If user is not logged in, redirect to homepage.
    If form input is valid, redirect to user detail page.
    If form input is not valid, redirect to the note add form."""

    form = NoteAddForm()

    if 'username' not in session:  # move guard up
        return redirect('/')

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)

        db.session.add(note)
        db.session.commit()
        flash(f"Note has been added!")
        return redirect(f'/users/{username}')

    else:
        return render_template("note_add_form.html", form=form)


@app.route('/notes/<int:note_id>/update', methods=["POST", "GET"])
def note_edit(note_id):
    """Allow user to edit note.
    If user is not logged in, redirect to homepage.
    If form input is valid, redirect to user detail page.
    If form input is not valid, redirect to the note edit form page."""

    note = Note.query.get_or_404(note_id)

    # user = User.query.get(username)
    form = NoteEditForm(obj=note)

    if 'username' not in session:  # move guard up
        return redirect("/")

    if form.validate_on_submit():
        note.title = form.title.data or note.title
        note.content = form.content.data or note.content
        db.session.commit()

        username = session['username']

        flash(f"Note has been edited!")
        return redirect(f'/users/{username}')

    else:
        return render_template('note_edit_form.html', form=form)


@app.post('/notes/<int:note_id>/delete')
def note_delete(note_id):
    """Allow user to delete note.
    If user is not logged in, redirect to homepage.
    If form input is valid, redirect to user detail page
    If form input is not valid, redirect to user detail page."""

    form = CSRFForm()

    note = Note.query.get_or_404(note_id)

    if 'username' not in session:  # move guard up
        return redirect("/")

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        username = session['username']

        flash(f"Note has been deleted!")
        return redirect(f'/users/{username}')
    else:
        return redirect(f'/users/{username}')
