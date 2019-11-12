import os
import config
from flask import Flask
from flask_login import LoginManager, logout_user
from flask_wtf.csrf import CSRFProtect
from models.base_model import db
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

# CSRF protection
csrf = CSRFProtect(app)
# CSRF protection ends

# Flask login
login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = "sessions.new"
login_manager.login_message = "Please log in before proceed"
login_manager.login_message_category = "alert alert-warning"

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)
# Flask login ends

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


