import peewee as pw
import config as cfg
from flask_login import UserMixin
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property, hybrid_method

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    image_path = pw.CharField(default="profile-placeholder.jpg")

    def validate(self):
        #-----------------------------------
        # Logic for validation
        #-----------------------------------
        # if user is found in database
        #     if user found in database is self
        #         must be user editing username, allow it to pass
        #         impossible to be new user
        #     else
        #         could be new user who picked an existing username, should not pass
        #         could be exising user who changed to an exisiting username, should not pass
        # else
        #     could be new user or user editing username, allow it to pass

        # Check username
        user = User.get_or_none(User.username == self.username)
        if user:
            if user != self:
                self.errors.append("This username has been chosen")

        # Check email
        user = User.get_or_none(User.email == self.email)
        if user:
            if user != self:
                self.errors.append("This email has been registered with another account")

    @hybrid_property
    def profile_image_url(self):
        return cfg.S3_LOCATION + self.image_path
            
        