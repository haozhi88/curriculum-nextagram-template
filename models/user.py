from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=False)
    password = pw.CharField(unique=False)

    def validate(self):
        print("user validate")