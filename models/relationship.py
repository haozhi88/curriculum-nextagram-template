from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property, hybrid_method

class Relationship(BaseModel):
    idol_id = pw.ForeignKeyField(User, backref='idols', on_delete="CASCADE")
    fan_id = pw.ForeignKeyField(User, backref='fans', on_delete="CASCADE")
    approve = pw.BooleanField(default=False)

            
        