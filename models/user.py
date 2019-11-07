from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        # Check username
        user = User.get_or_none(User.username == self.username)
        if user:
            self.errors.append("This username has been chosen")

        # Check email
        user = User.get_or_none(User.email == self.email)
        if user:
            self.errors.append("This email has been registered with another account")
        