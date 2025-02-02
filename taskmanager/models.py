from django.db import models
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, DictField
from datetime import datetime

from usermanager.models import User

class Item(Document):
    name = StringField(required=True)

class Task(Document):
    title = StringField(required=True)
    group = StringField(required=True)
    description = StringField(required=True)
    items = ListField(ReferenceField(Item), default=list)
    editors = ListField(ReferenceField(User), default=list)
    created_at = DateTimeField(default=datetime.now)
    last_modification_time = DateTimeField(default=None)

    meta = {'collection': 'tasks'}