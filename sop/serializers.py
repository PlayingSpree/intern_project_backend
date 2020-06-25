from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Post, Step, StepFile
from djoser.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator']
        read_only_fields = ['id', 'creator']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'name', 'textcontent', 'link', 'cover_type', 'cover_file', 'post_id']
        read_only_fields = ['id']


class StepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepFile
        fields = ['id', 'step_id', 'file']
        read_only_fields = ['id']
