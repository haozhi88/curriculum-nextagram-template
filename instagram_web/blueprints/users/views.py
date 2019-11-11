import config as cfg
from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from helpers import s3
from models.user import User
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

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(cfg.S3_LOCATION, file.filename)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    # session_id = session.get('id') # flask-session
    session_id = current_user.get_id() # flask-login
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
        flash('Unauthorized user', 'alert alert-danger')
        return render_template('users/edit.html', username=username, email=email, id=id)

@users_blueprint.route('/<id>/newimage', methods=['GET'])
def newimage(id):
    return render_template('users/newimage.html')

@users_blueprint.route('/<id>/newimage', methods=['POST'])
def uploadimage(id):
    # Check for authorized user
    user = User.get_or_none(User.id==id)

    if user.id == current_user.id:
        if "user_file" not in request.files:
            flash('No user_file key in request.files', 'alert alert-danger')
            return redirect(url_for('users.newimage'))

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
            return redirect(url_for('users.newimage'))

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file, cfg.S3_BUCKET)
            print(f"filename: {file.filename}")
            print(f"output: {output}")
            user.image_path = file.filename
            if user.save():
                flash('Upload successful', 'alert alert-success')
                return redirect(url_for('users.edit', id=id))
            else:
                flash('Upload failed', 'alert alert-danger')
                error_to_flash(user.errors)
                return redirect(url_for('users.newimage'))
        else:
            flash('Upload failed', 'alert alert-danger')
            return redirect(url_for('users.newimage'))