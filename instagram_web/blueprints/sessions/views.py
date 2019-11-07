from flask import Blueprint, render_template, request, redirect, url_for, flash
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

@sessions_blueprint.route('/', methods=['POST'])
def create():
    # Fetch values from sign in form
    username = request.form.get('username')
    password = generate_password_hash(request.form.get('password'))

    user = User.get_or_none(User.username == username)
    if user:
        print("user exist")
        print(f"input pw: {password}")
        print(f"user pw: {user.password}")
        result = check_password_hash(password, user.password)
        if result:
            print(f"result is true")
        else:
            print(f"result is false")
    else:
        print("user not exist")

    return redirect(url_for('home'))

    # Create new user
    # user = User(username=username, email=email, password=password)
    # if user.save():
    #     flash('New user created', 'alert alert-primary')
    #     return redirect(url_for('home'))
    # else:
    #     error_to_flash(user.errors)
    #     return render_template('users/new.html', username=username, email=email)


