from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property, hybrid_method

class Relationship(BaseModel):
    idol = pw.ForeignKeyField(User, backref='idols', on_delete="CASCADE")
    fan = pw.ForeignKeyField(User, backref='fans', on_delete="CASCADE")
    status = pw.CharField(default='pending') # pending -> approve -> block

    def is_exist(self):
        query = Relationship.select().where(Relationship.idol==self.idol, Relationship.fan==self.fan)
        if len(query):
            return True
        else:
            return False
        