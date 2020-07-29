from rest_framework import serializers

from authapp.serializers import UserDataSerializer
from .models import Session, Step, StepFile, Course, SopHistory


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
        fields = ['id', 'name', 'textcontent', 'link', 'cover_type', 'cover_file', 'post_id', 'step_file',
                  'date_created', 'date_modified']
        read_only_fields = ['id', 'step_file', 'date_created', 'date_modified']


class SessionSerializer(serializers.ModelSerializer):
    creator = UserDataSerializer(source='creator_id', read_only=True)
    step = serializers.SerializerMethodField(read_only=True)

    def get_step(self, obj):
        serializer = StepSerializer(Step.objects.filter(post_id=obj.id), many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'step', 'date_created', 'date_modified']
        read_only_fields = ['id', 'creator', 'step', 'date_created', 'date_modified']


class CourseSerializer(serializers.ModelSerializer):
    creator = UserDataSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'posts', 'date_created', 'date_modified']
        read_only_fields = ['id', 'creator', 'date_created', 'date_modified']


class SopHistorySerializer(serializers.ModelSerializer):
    user = UserDataSerializer(source='user_id', read_only=True)
    post = SessionSerializer(source='post_id', read_only=True)
    class Meta:
        model = SopHistory
        fields = ['user', 'post', 'datetime']
        # read_only_fields = ['user_id', 'post_id', 'step_id', 'datetime']