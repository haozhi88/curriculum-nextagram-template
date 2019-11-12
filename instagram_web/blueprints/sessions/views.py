from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

sessions_blueprint = Blueprint('sessions',
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
@sessions_blueprint.route('/signin', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/signin', methods=['POST'])
def create():
    # Fetch values from sign in form
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_or_none(User.username == username)
    if user:
        # check_password_hash(arg1: hashed_pw, arg2: pw_string)
        result = check_password_hash(user.password, password)
        if result:
            # session['id'] = user.id # flask-session
            login_user(user) # flask-login
            flash('Successfully logged in', 'alert alert-success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect password', 'alert alert-danger')
            return render_template('/sessions/new.html', username=username)
    else:
        flash('User not exist', 'alert alert-danger')
        return render_template('/sessions/new.html', username=username)

@sessions_blueprint.route('/delete', methods=['GET'])
def destroy():
    # session.pop('id', None) # flask-session
    logout_user() # flask-login
    flash('Successfully logged out', 'alert alert-warning') 
    return redirect(url_for('home'))

# <form action="{{ url_for('sessions.destroy') }}" method="POST">
#     <input class="nav-link" value="Sign Out" type="submit" />
# </form>


