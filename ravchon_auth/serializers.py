from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        return user