import config as cfg
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property, hybrid_method

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images', on_delete="CASCADE")
    image_path = pw.CharField(null=False)

    @hybrid_property
    def image_url(self):
        return cfg.S3_LOCATION + self.image_path
            
        