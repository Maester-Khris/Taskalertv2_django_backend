from rest_framework import serializers 
from .models import Task

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB uses ObjectId
    name = serializers.CharField(max_length=100)
    group = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        task = Task(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.group = validated_data.get('group', instance.group)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance