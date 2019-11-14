from app import app
from flask import render_template, redirect, url_for
from helpers.google_oauth import oauth
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.payment.views import payment_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
import os
import config

# Flask assets
assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(payment_blueprint, url_prefix="/payment")
app.register_blueprint(sessions_blueprint, url_prefix="/")

# O'Auth
oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/")
def home():
    # return render_template('home.html')
    return redirect(url_for('users.index')) 

