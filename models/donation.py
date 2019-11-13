import config as cfg
from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw

class Donation(BaseModel):
    receiver = pw.ForeignKeyField(User, backref='receiver_donations', on_delete="CASCADE")
    donor = pw.ForeignKeyField(User, backref='donor_donations', on_delete="CASCADE")
    image = pw.ForeignKeyField(Image, backref='image_donations', on_delete="CASCADE")
    amount = pw.IntegerField(null=False) # USD 1 = 100


