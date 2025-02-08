from rest_framework import serializers 
from .models import User
from datetime import datetime

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, required=False)  # MongoDB uses ObjectId
    name = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(default=datetime.now, read_only=True)

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # The created_at field should not be updated
        instance.save()
        return instance