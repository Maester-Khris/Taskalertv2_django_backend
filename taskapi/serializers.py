from rest_framework import serializers 
from .models import Task, Item
from datetime import datetime
from userapi.serializers import UserSerializer
from userapi.models import User

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB uses ObjectId
    title = serializers.CharField(max_length=100)
    group = serializers.CharField(max_length=100)
    description = serializers.CharField()  # No max_length for text
    items = ItemSerializer(many=True, required=False)  # List of items
    editors = UserSerializer(many=True, required=False)  # List of editors
    created_at = serializers.DateTimeField(default=datetime.now, read_only=True)
    last_modification_time = serializers.DateTimeField(default=None, allow_null=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        editors_data = validated_data.pop('editors', [])
        task = Task(**validated_data)
        task.save()

        for item_data in items_data:
            item = Item(**item_data)
            item.save()
            task.items.append(item)

        for editor_data in editors_data:
            editor = User(**editor_data)
            editor.save()
            task.editors.append(editor)

        task.save()
        return task

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        editors_data = validated_data.pop('editors', None)

        instance.title = validated_data.get('title', instance.title)
        instance.group = validated_data.get('group', instance.group)
        instance.description = validated_data.get('description', instance.description)

        if items_data is not None:
            instance.items.clear()  # Clear existing items
            for item_data in items_data:
                item = Item(**item_data)
                item.save()
                instance.items.append(item)

        if editors_data is not None:
            instance.editors.clear()  # Clear existing editors
            for editor_data in editors_data:
                editor = User(**editor_data)
                editor.save()
                instance.editors.append(editor)

        instance.last_modification_time = datetime.now()  # Update last modification time
        instance.save()
        return instance
    
