from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from models.user import User
from models.relationship import Relationship

relationship_blueprint = Blueprint('relationship',
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
@relationship_blueprint.route('/followers', methods=['GET'])
@login_required
def show_fan():
    if current_user.is_authenticated:
        user = User.get_or_none(User.id==current_user.id)
        fans = User.select().join(Relationship, on=(Relationship.fan_id==User.id)).where(Relationship.idol_id==user.id)
        return render_template('relationship/show_fan.html', fans=fans)
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/following', methods=['GET'])
@login_required
def show_idol():
    if current_user.is_authenticated:
        user = User.get_or_none(User.id==current_user.id)
        idols = User.select().join(Relationship, on=(Relationship.idol_id==User.id)).where(Relationship.fan_id==user.id)
        return render_template('relationship/show_idol.html', idols=idols)
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/<idol_id>/follow', methods=['POST'])
@login_required
def follow(idol_id):
    if current_user.is_authenticated:
        fan = User.get_or_none(User.id==current_user.id)
        idol = User.get_or_none(User.id==idol_id)
        if fan and idol:        
            relationship = Relationship(fan=fan, idol=idol)
            if not relationship.is_exist():
                if not idol.private:
                    relationship.status = "approve"
                if relationship.save():
                    flash('Follow profile successful', 'alert alert-success')
                    return redirect(url_for('users.show', id_or_username=idol.username))
            else:
                flash('Profile has been followed', 'alert alert-danger')
        else:
            flash('Follow profile failed', 'alert alert-danger')
        return redirect(url_for('users.show', id_or_username=idol.username))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/<idol_id>/unfollow', methods=['POST'])
@login_required
def unfollow(idol_id):
    if current_user.is_authenticated:
        fan = User.get_or_none(User.id==current_user.id)
        idol = User.get_or_none(User.id==idol_id)
        if fan and idol:
            query = Relationship.select().where(Relationship.idol==idol, Relationship.fan==fan) 
            if len(query):
                relationship = query[0]
                if relationship.delete_instance():
                    flash('Unfollow profile successful', 'alert alert-success')
                    return redirect(url_for('users.show', id_or_username=idol.username))
                else:
                    flash('Unfollow profile failed', 'alert alert-danger')
            else:
                flash('Profile has not been followed', 'alert alert-danger')
        else:
            flash('Unfollow profile failed', 'alert alert-danger')
        return redirect(url_for('users.show', id_or_username=idol.username))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/<id>/approve', methods=['POST'])
@login_required
def approve(id):
    pass

@relationship_blueprint.route('/<id>/block', methods=['POST'])
@login_required
def block(id):
    pass