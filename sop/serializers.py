from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Post, Step, StepFile


class StepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepFile
        fields = ['id', 'step_id', 'file']
        read_only_fields = ['id']


class StepSerializer(serializers.ModelSerializer):
    step_file = serializers.SerializerMethodField(read_only=True)

    def get_step_file(self, obj):
        serializer = StepFileSerializer(StepFile.objects.filter(step_id=obj.id), many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Step
        fields = ['id', 'name', 'textcontent', 'link', 'cover_type', 'cover_file', 'post_id', 'step_file']
        read_only_fields = ['id', 'step_file']


class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(source='creator_id', read_only=True)
    step = serializers.SerializerMethodField(read_only=True)

    def get_step(self, obj):
        serializer = StepSerializer(Step.objects.filter(post_id=obj.id), many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Post
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'step']
        read_only_fields = ['id', 'creator', 'step']
