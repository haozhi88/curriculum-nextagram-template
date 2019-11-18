from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from helpers.sendgrid import *
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
        approve_fans = User.select().join(Relationship, on=(Relationship.fan_id==User.id)).where(Relationship.idol_id==user.id, Relationship.status=="approve")
        pending_fans = User.select().join(Relationship, on=(Relationship.fan_id==User.id)).where(Relationship.idol_id==user.id, Relationship.status=="pending")
        return render_template('relationship/show_fan.html', approve_fans=approve_fans, pending_fans=pending_fans)
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/following', methods=['GET'])
@login_required
def show_idol():
    if current_user.is_authenticated:
        user = User.get_or_none(User.id==current_user.id)
        approve_idols = User.select().join(Relationship, on=(Relationship.idol_id==User.id)).where(Relationship.fan_id==user.id, Relationship.status=="approve")
        pending_idols = User.select().join(Relationship, on=(Relationship.idol_id==User.id)).where(Relationship.fan_id==user.id, Relationship.status=="pending")
        return render_template('relationship/show_idol.html', approve_idols=approve_idols, pending_idols=pending_idols)
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
                if idol.private:
                    # send_email(f"{fan.username} has followed you on nextagram! Approve follow request to allow profile view.")
                    pass
                else:
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
            relationship = Relationship.get_or_none(Relationship.fan==fan, Relationship.idol==idol)
            if relationship:
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

@relationship_blueprint.route('/<fan_id>/approve', methods=['POST'])
@login_required
def approve(fan_id):
    if current_user.is_authenticated:
        fan = User.get_or_none(User.id==fan_id)
        idol = User.get_or_none(User.id==current_user.id)
        if fan and idol:
            relationship = Relationship.get_or_none(Relationship.fan==fan, Relationship.idol==idol)
            if relationship and relationship.status == "pending":
                if Relationship.update(status = "approve").where(Relationship.id==relationship.id).execute():
                    flash('Approve follower successful', 'alert alert-success')
                else:
                    flash('Approve follower failed', 'alert alert-danger')
            else:
                flash('Profile has not been followed', 'alert alert-danger')
        else:
            flash('Unfollow profile failed', 'alert alert-danger')
        return redirect(url_for('relationship.show_fan'))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@relationship_blueprint.route('/<fan_id>/block', methods=['POST'])
@login_required
def block(fan_id):
    if current_user.is_authenticated:
        fan = User.get_or_none(User.id==fan_id)
        idol = User.get_or_none(User.id==current_user.id)
        if fan and idol:
            relationship = Relationship.get_or_none(Relationship.fan==fan, Relationship.idol==idol)
            if relationship:
                if relationship.delete_instance():
                    flash('Block profile successful', 'alert alert-success')
                else:
                    flash('Block profile failed', 'alert alert-danger')
            else:
                flash('Profile has not been followed', 'alert alert-danger')
        else:
            flash('Block profile failed', 'alert alert-danger')
        return redirect(url_for('relationship.show_fan'))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))