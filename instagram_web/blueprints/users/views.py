from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from helpers_braintree import *
from helpers_sendgrid import *
from helpers_s3 import *
from models.user import User
from models.image import Image
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

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

@users_blueprint.route('/new', methods=['POST'])
def create():
    # Fetch values from sign up form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform validation

    # Create new user
    user = User(username=username, email=email, password=password)
    if user.save():
        flash('New user created', 'alert alert-success')
        return redirect(url_for('home'))
    else:
        error_to_flash(user.errors)
        return render_template('users/new.html', username=username, email=email)

def show_profile(id_or_username, is_profile):
    # TODO: for private profile, need to get session and check current user id

    # Get user by id or username
    if id_or_username.isdigit():
        user = User.get_or_none(User.id==id_or_username)
    else:
        user = User.get_or_none(User.username==id_or_username)
    
    # Render page if user exist
    if user:
        # Get list of images
        images = user.images
        return render_template('users/show.html', user=user, images=images)
    else:
        flash('User not exist', 'alert alert-danger')
        return redirect(url_for('home'))  

@users_blueprint.route('/<id_or_username>', methods=["GET"])
def show(id_or_username):
    return show_profile(id_or_username, False) 

@users_blueprint.route('/profile', methods=["GET"])
@login_required
def show_myprofile():
    session_id = current_user.get_id() # flask-login
    if session_id:
        return show_profile(str(session_id), True)
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@users_blueprint.route('/', methods=["GET"])
def index():
    users = User.select().order_by(User.id.asc())
    return render_template('users/index.html', users=users)

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    # session_id = session.get('id') # flask-session
    session_id = current_user.get_id() # flask-login
    if session_id:
        user = User.get_or_none(User.id==id)
        if user and session_id==user.id:
            username=user.username
            email=user.email
            private=user.private
            return render_template('users/edit.html', username=username, email=email, private=private, id=id)
        else:
            flash('Unauthorized user', 'alert alert-danger')
            return redirect(url_for('home'))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    # Fetch values from sign up form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if request.form.get('private') == "on":
        private = True
    else:
        private = False

    # Perform validation

    # Check for authorized user
    user = User.get_or_none(User.id==id)
    if user.id == current_user.id:
        user.username = username
        user.email = email
        user.password = password
        user.private = private
        if user.save():
            flash('Update successful', 'alert alert-success')
            return redirect(url_for('users.edit', id=id))
        else:
            flash('Update failed', 'alert alert-danger')
            error_to_flash(user.errors)
            return render_template('users/edit.html', username=username, email=email, private=private, id=id)
    else:        
        flash('Unauthorized user', 'alert alert-danger')
        return render_template('users/edit.html', username=username, email=email, private=private, id=id)

@users_blueprint.route('/<id>/newimage', methods=['GET'])
@login_required
def newimage(id):
    return render_template('users/newimage.html')

@users_blueprint.route('/<id>/newimage', methods=['POST'])
@login_required
def uploadimage(id):
    # Check for authorized user
    user = User.get_or_none(User.id==id)

    if user.id == current_user.id:
        if "user_file" not in request.files:
            flash('No user_file key in request.files', 'alert alert-danger')
            return redirect(url_for('users.newimage', id=id))

        file    = request.files["user_file"]

        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """

        if file.filename == "":
            flash('Please select a file', 'alert alert-danger')
            return redirect(url_for('users.newimage', id=id))

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file, S3_BUCKET)
            if User.update(image_path = file.filename).where(User.id==user.id).execute():
                # send_email(f"{user.username} has uploaded a new image {file.filename}")
                flash('Upload successful', 'alert alert-success')
                return redirect(url_for('users.edit', id=id))

    flash('Upload failed', 'alert alert-danger')
    return redirect(url_for('users.newimage', id=id))