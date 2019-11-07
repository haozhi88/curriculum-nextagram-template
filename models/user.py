from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=False)
    password = pw.CharField(unique=False)

    def validate(self):
        user = User.get_or_none(User.username == self.username)
        if user:
            self.errors.append("Username has been chosen")