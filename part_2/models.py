from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, BooleanField


class User(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    send_email = BooleanField(default=False)