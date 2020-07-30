import os

from rest_framework import serializers

from authapp.serializers import UserDataSerializer
from .models import Session, Step, StepFile, Course, SopHistory


class StepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepFile
        fields = ['id', 'step_id', 'file']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        file = {
            "url": representation.pop("file"),
            "size": instance.file.size,
            "name": os.path.basename(instance.file.name),
        }
        representation['file'] = file
        return representation


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
        serializer = StepSerializer(Step.objects.filter(post_id=obj.id), many=True, read_only=True,
                                    context={"request": self.context.get('request')})
        return serializer.data

    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'step', 'date_created', 'date_modified']
        read_only_fields = ['id', 'creator', 'step', 'date_created', 'date_modified']


class SessionWithNoStepSerializer(serializers.ModelSerializer):
    creator = UserDataSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'date_created', 'date_modified']
        read_only_fields = ['id', 'creator', 'date_created', 'date_modified']


class CourseSerializer(serializers.ModelSerializer):
    creator = UserDataSerializer(source='creator_id', read_only=True)
    progress = serializers.SerializerMethodField(read_only=True)

    def get_progress(self, obj):
        if(obj.posts.count()==0):
            return 0
        return round(SopHistory.objects.filter(post_id__course=obj).count() / obj.posts.count() * 100, 2)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'cover', 'publish', 'creator', 'posts', 'progress', 'date_created',
                  'date_modified']
        read_only_fields = ['id', 'creator', 'date_created', 'date_modified']


class SopHistorySerializer(serializers.ModelSerializer):
    session = SessionWithNoStepSerializer(source='post_id', read_only=True)

    class Meta:
        model = SopHistory
        fields = ['session', 'datetime']
