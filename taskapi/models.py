from django.db import models
from mongoengine import Document, StringField, IntField

class Task(Document):
    name = StringField(required=True, max_length=100)
    group = StringField(required=True, max_length=100)
    description = StringField(required=True, max_length=255)

    meta = {'collection': 'tasks'}  # Specify the collection name

# class Task(models.Model):
#     name = models.CharField(max_length=70, blank=False, default='')
#     description = models.CharField(max_length=70, blank=False, default='')
#     group = models.CharField(max_length=200,blank=False, default='')

#     def __str__(self):
#         return self.title