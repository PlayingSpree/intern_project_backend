from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Post
from djoser.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'creator_id']
        read_only_fields = ['id', 'creator']
        extra_kwargs = {'creator_id': {'write_only': True}}