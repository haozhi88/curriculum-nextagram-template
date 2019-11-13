from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from helpers.braintree import *
from helpers.s3 import *
from models.user import User
from models.image import Image
from models.donation import Donation

payment_blueprint = Blueprint('payment',
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
@payment_blueprint.route('/new/<id>', methods=['GET'])
@login_required
def new(id):
    if current_user.is_authenticated:
        client_token = generate_client_token()
        image = Image.get_or_none(Image.id==id)
        receiver = image.user
        return render_template('payment/new.html', client_token=client_token, id=id)
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))

@payment_blueprint.route('/<transaction_id>', methods=['GET'])
@login_required
def show(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('payment/show.html', transaction=transaction, result=result)

@payment_blueprint.route('/<id>', methods=['POST'])
@login_required
def create(id):
    if current_user.is_authenticated:
        amount = int(request.form.get('amount'))
        result = transact({
            'amount': amount,
            'payment_method_nonce': request.form['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            image = Image.get_or_none(Image.id==id)
            receiver = image.user
            donor = User.get_by_id(current_user.id)
            amount = amount*100
            donation = Donation(receiver=receiver, donor_id=donor.id, image=image, amount=amount)
            if donation.save():
                # print(f"donor: {donation.donor.username}")
                # print(f"receiver: {donation.receiver.username}")
                # print(f"amount: {donation.amount}")
                flash('Donation successful', 'alert alert-success')
                return redirect(url_for('home'))
            else:
                flash('Donation unsuccessful', 'alert alert-danger')
                return redirect(url_for('home'))
        else:
            for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
            return redirect(url_for('payment.new', id=id))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))


