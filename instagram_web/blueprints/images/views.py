from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from helpers_s3 import *
from models.user import User
from models.image import Image
from werkzeug.utils import secure_filename

images_blueprint = Blueprint('images',
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
@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    if current_user.is_authenticated:
        return render_template('images/new.html')
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))


@images_blueprint.route('/new', methods=['POST'])
@login_required
def create():
    if current_user.is_authenticated:
        user = User.get_or_none(User.id==current_user.id)
        if "user_file" not in request.files:
            flash('No user_file key in request.files', 'alert alert-danger')
            return redirect(url_for('images.new'))

        file    = request.files["user_file"]

        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file, S3_BUCKET)
            # User.update(image_path = file.filename).where(User.id==user.id).execute()
            image = Image(user=user, image_path=file.filename)
            if image.save():
                flash('Upload successful', 'alert alert-success')
                return redirect(url_for('users.show', id_or_username=current_user.username))

        flash('Upload failed', 'alert alert-danger')
        return redirect(url_for('images.new'))

    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@images_blueprint.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    if current_user.is_authenticated:
        image = Image.get_or_none(Image.id==id)
        if image.user == User.get_or_none(User.id==current_user.id):
            if image:
                image.delete_instance()
                flash('Image successfully deleted', 'alert alert-success')
            else:
                flash('Image not exist', 'alert alert-danger')
        else:
            flash('No permission to delete', 'alert alert-danger')
        return redirect(url_for('users.show', id_or_username=current_user.username))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

    











