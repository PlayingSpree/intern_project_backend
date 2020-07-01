from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Assignment, AssignmentFile, AssignmentWorkFile, AssignmentWork


# create group
class AssignmentSerializer(serializers.ModelSerializer):
    admin = UserSerializer(source='admin_id', read_only=True)
    assignment_files = serializers.SerializerMethodField(read_only=True)

    def get_assignment_files(self, obj):
        serializer = AssignmentFileSerializer(AssignmentFile.objects.filter(assignment_id=obj.id), many=True,
                                              read_only=True)
        return serializer.data

    class Meta:
        model = Assignment
        fields = ['id', 'group_id', 'admin', 'assignment_files', 'name', 'description']
        read_only_fields = ['id', 'admin']


class AssignmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFile
        fields = ['id', 'assignment_id', 'file']
        read_only_fields = ['id']


class AssignmentWorkSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    work_files = serializers.SerializerMethodField(read_only=True)

    def get_work_files(self, obj):
        serializer = AssignmentWorkFileSerializer(AssignmentWorkFile.objects.filter(assignment_work_id=obj.id),
                                                  many=True,
                                                  read_only=True)
        return serializer.data

    class Meta:
        model = AssignmentWork
        fields = ['id', 'assignment_id', 'user', 'user_id', 'work_files', 'text']
        read_only_fields = ['id', 'work_files']
        extra_kwargs = {'user_id': {'write_only': True}}


class AssignmentWorkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentWorkFile
        fields = ['id', 'assignment_work_id', 'file']
        read_only_fields = ['id']
