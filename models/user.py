import peewee as pw
import config as cfg
from flask_login import UserMixin
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property, hybrid_method
from werkzeug.security import generate_password_hash

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    role = pw.CharField(default="user")
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
                self.errors.append("Username not unique")

        # Check email
        user = User.get_or_none(User.email == self.email)
        if user:
            if user != self:
                self.errors.append("Email not unique")

        # Check password
        # self.password = generate_password_hash(self.password)
        if len(self.password) < 3 or len(self.password) > 25:
            print(f"debug password: {self.password}")
            self.errors.append("Password must be between 3~25 characters")
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def profile_image_url(self):
        return cfg.S3_LOCATION + self.image_path
            
        