from django.db import models
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {'collection': 'users'}

    def __str__(self):
        return self.title
