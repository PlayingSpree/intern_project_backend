import os

from djoser.serializers import UserSerializer
from rest_framework import serializers

from authapp.serializers import UserDataSerializer
from .models import Assignment, AssignmentFile, AssignmentWorkFile, AssignmentWork


# create group
class AssignmentSerializer(serializers.ModelSerializer):
    admin = UserDataSerializer(source='admin_id', read_only=True)
    assignment_files = serializers.SerializerMethodField(read_only=True)
    turn_in_count = serializers.SerializerMethodField(read_only=True)

    def get_assignment_files(self, obj):
        serializer = AssignmentFileSerializer(AssignmentFile.objects.filter(assignment_id=obj.id), many=True,
                                              read_only=True)
        return serializer.data

    def get_turn_in_count(self, obj):
        AssignmentWork.objects.filter(assignment_id=obj.pk).count()

    class Meta:
        model = Assignment
        fields = ['id', 'group_id', 'admin', 'assignment_files', 'name', 'description', 'turn_in_count', 'date_created',
                  'date_modified', 'due_date', 'allow_file']
        read_only_fields = ['id', 'admin', 'date_created', 'date_modified']


class AssignmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFile
        fields = ['id', 'assignment_id', 'file']
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


class AssignmentWorkSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(source='user_id', read_only=True)
    work_files = serializers.SerializerMethodField(read_only=True)

    def get_work_files(self, obj):
        serializer = AssignmentWorkFileSerializer(AssignmentWorkFile.objects.filter(assignment_work_id=obj.id),
                                                  many=True, read_only=True)
        return serializer.data

    class Meta:
        model = AssignmentWork
        fields = ['id', 'assignment_id', 'user', 'user_id', 'work_files', 'text', 'date_created', 'date_modified']
        read_only_fields = ['id', 'work_files', 'date_created', 'date_modified']
        extra_kwargs = {'user_id': {'write_only': True}}


class AssignmentWorkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentWorkFile
        fields = ['id', 'assignment_work_id', 'file']
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
