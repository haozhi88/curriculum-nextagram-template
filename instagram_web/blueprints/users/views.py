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
    password = request.form.get('password')

    # Perform validation

    # Create new user
    password = generate_password_hash(password)
    user = User(username=username, email=email, password=password)
    if user.save():
        flash('New user created', 'alert alert-success')
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
    # Fetch values from sign up form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform validation

    # Check for authorized user
    user = User.get_or_none(User.id==id)
    if user.id == current_user.id:
        user.username = username
        user.email = email
        user.password = generate_password_hash(password)
        if user.save():
            flash('Update successful', 'alert alert-success')
            return redirect(url_for('users.edit', id=id))
        else:
            flash('Update failed', 'alert alert-danger')
            error_to_flash(user.errors)
            return render_template('users/edit.html', username=username, email=email, id=id)
    else:
        print(f"error user name: {user.username}, user id: {user.id}, current_user name: {current_user.username}, current_user id: {current_user.id}")
        flash('Unauthorized user', 'alert alert-danger')
        return render_template('users/edit.html', username=username, email=email, id=id)

