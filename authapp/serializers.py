from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from authapp.models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone')

