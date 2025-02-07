from django.db import models
from mongoengine import  Document, StringField, ListField, DateTimeField, DictField, ReferenceField
from userapi.models import User
from datetime import datetime

class Item(Document):
    name = StringField(required=True)
    meta = {'collection': 'items'}

    def __str__(self):
        return self.name

class Task(Document):
    title = StringField(required=True, max_length=100)
    group = StringField(required=True, max_length=100)
    description = StringField(required=False)  # No max_length for text
    items = ListField(ReferenceField(Item), default=list)  # List of Item references
    editors = ListField(ReferenceField(User))  # List of User references
    created_at = DateTimeField(default=datetime.now)
    last_modification_time = DateTimeField(default=None)

    meta = {'collection': 'tasks'}

    def __str__(self):
        return self.title
    
