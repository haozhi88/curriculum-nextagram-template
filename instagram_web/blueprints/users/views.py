from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

"""""""""""""""""""""""""""""""""
Others
"""""""""""""""""""""""""""""""""
def error_to_flash(errors):
    for error in errors:
        flash(error, 'alert alert-danger')

"""""""""""""""""""""""""""""""""
Route functions
"""""""""""""""""""""""""""""""""
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    # Fetch values from sign up form
    username = request.form.get('username')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'))

    # Create new user
    user = User(username=username, email=email, password=password)
    if user.save():
        flash('New user created', 'alert alert-primary')
        return redirect(url_for('home'))
    else:
        error_to_flash(user.errors)
        return render_template('users/new.html', username=username, email=email)

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    # session_id = session.get('id') # method 1: manual
    session_id = current_user.get_id() # method 2: flask-login
    if session_id:
        user = User.get_or_none(User.id==id)
        if user and session_id==user.id:
            username=user.username
            email=user.email
            return render_template('users/edit.html', username=username, email=email, id=id)            
        else:
            flash('Unauthorized user', 'alert alert-danger')
            return redirect(url_for('home'))
    else:
        flash('Not logged in', 'alert alert-danger')
        return redirect(url_for('home'))

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
