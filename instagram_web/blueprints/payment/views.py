from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from helpers_braintree import *
from models.user import User
from models.image import Image

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
        result = transact({
            'amount': request.form['amount'],
            'payment_method_nonce': request.form['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        image = Image.get_or_none(Image.id==id)
        receiver = image.user
        print(f"create image id: {image.id}, image path: {image.image_path}")
        print(f"create donater: {current_user.username}")
        print(f"create receiver: {receiver.username}")

        if result.is_success or result.transaction:
            flash('Donate successful', 'alert alert-success')
            return redirect(url_for('home'))
        else:
            for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
            return redirect(url_for('payment.new', id=id))
    else:
        flash('Log in required', 'alert alert-danger')
        return redirect(url_for('home'))


