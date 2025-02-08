from django.db import models
from mongoengine import  Document, EmbeddedDocument, StringField, ListField, DateTimeField, DictField, ReferenceField, EmbeddedDocumentField
from userapi.models import User
from datetime import datetime


class Task(Document):
    title = StringField(required=True, max_length=100)
    group = ListField(StringField(required=True, max_length=100))
    description = StringField(required=False)  # No max_length for text
    items = ListField(StringField(), default=list)  # List of Item references
    editors = ListField(ReferenceField(User))  # List of User references
    created_at = DateTimeField(default=datetime.now)
    last_modification_time = DateTimeField(required=False, default=None)

    meta = {'collection': 'tasks'}

    def __str__(self):
        return self.title
    
