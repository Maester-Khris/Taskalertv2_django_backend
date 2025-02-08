from rest_framework import serializers
from .models import Task
from datetime import datetime
from userapi.serializers import UserSerializer
from userapi.models import User
from django.core.exceptions import ObjectDoesNotExist

# class ItemSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True)

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, read_only=True)  # MongoDB uses ObjectId
    title = serializers.CharField(max_length=100)
    group = serializers.ListField()
    description = serializers.CharField()  # No max_length for text
    items = serializers.ListField()  # List of items
    editors = UserSerializer(many=True, required=False)  # List of editors
    created_at = serializers.DateTimeField(required=False, default=datetime.now, read_only=True)
    last_modification_time = serializers.DateTimeField(required=False, default=None, allow_null=True)

    def clean(self):
        # Si aucun item n'est ajouté, initialise items avec une liste vide
        if self.items is None:
            self.items = []

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        editors_data = validated_data.pop('editors', [])
        task = Task(**validated_data)
        task.items.extend(items_data)
        task.save()
            
        for editor_data in editors_data:
            editor = User(**editor_data)
            editor.save()
            task.editors.append(editor)

        task.save()
        return task


    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        group_data = validated_data.pop('group', None)
        editors_data = validated_data.pop('editors', None)

        instance.title = validated_data.get('title', instance.title)
        instance.group = validated_data.get('group', instance.group)
        instance.description = validated_data.get('description', instance.description)

        if items_data is not None:
            instance.items.clear() # Clear existing items
            instance.items.extend(items_data)  

        # if group_data is not None:
        #     instance.group.clear() # Clear existing items
        #     instance.group.extend(group_data)

        if editors_data is not None:
            instance.editors.clear()  # Clear existing editors
            # for editor_data in editors_data:
            #     editor = User(**editor_data)
            #     editor.save()
            #     instance.editors.append(editor)

            for editor_data in editors_data:
                username = editor_data.get('name') 
                editor = User.objects(name=username)
                # if(editor ==  []):
                #     editor = User(**editor_data)
                #     editor.save()
                try:
                    editor = User.objects.get(name=username)
                except User.DoesNotExist:
                    editor = User(**editor_data)
                    editor.save()

                instance.editors.append(editor)



        instance.last_modification_time = datetime.now()  # Update last modification time
        instance.save()
        return instance
    
