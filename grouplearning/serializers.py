from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group, CommentGroup, CommentGroupFile, CommentGroupReply, CommentStep, CommentStepReply


# create group
class GroupSerializer(serializers.ModelSerializer):
    group_creator = UserSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_description', 'default_course', 'group_image', 'group_creator']
        read_only_fields = ['id', 'group_creator']


class CommentGroupFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGroupFile
        fields = ['id', 'comment_id', 'file']
        read_only_fields = ['id']


class CommentGroupSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer(source='user_id', read_only=True)
    comment_group_files = serializers.SerializerMethodField(read_only=True)

    def get_comment_group_files(self, obj):
        serializer = CommentGroupFileSerializer(CommentGroupFile.objects.filter(comment_id=obj.id), many=True,
                                                read_only=True)
        return serializer.data

    class Meta:
        model = CommentGroup
        fields = ['id', 'group_id', 'text', 'comment_group_files', 'commented_by']
        read_only_fields = ['id', 'commented_by', 'comment_group_files']


class CommentGroupReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentGroupReply
        fields = ['id', 'user', 'parent_id', 'text']
        read_only_fields = ['id']


class AddUserSerializer(serializers.ModelSerializer):
    user_joined = serializers.ListSerializer(child=serializers.IntegerField())

    class Meta:
        model = Group
        fields = ['id', 'user_joined']
        extra_kwargs = {'id': {'read_only': False}}


class CommentStepSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentStep
        fields = ['id', 'group_id', 'step_id', 'text', 'commented_by']
        read_only_fields = ['id', 'commented_by', 'step_id']


class CommentStepReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentStepReply
        fields = ['id', 'user', 'parent_id', 'text']
        read_only_fields = ['id']

