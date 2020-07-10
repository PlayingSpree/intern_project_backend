from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group, CommentGroup, CommentGroupFile, CommentGroupReply, CommentStep, CommentStepReply

User = get_user_model()


# create group
class GroupSerializer(serializers.ModelSerializer):
    group_creator = UserSerializer(source='creator_id', read_only=True)
    member_count = serializers.SerializerMethodField(read_only=True)

    def get_member_count(self, obj):
        return obj.user_joined.count()

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_description', 'member_count', 'courses', 'group_image', 'group_creator',
                  'date_created', 'date_modified']
        read_only_fields = ['id', 'group_creator', 'date_created', 'date_modified']


class CommentGroupFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGroupFile
        fields = ['id', 'comment_id', 'file']
        read_only_fields = ['id']


class CommentGroupSerializer(serializers.ModelSerializer):
    comment_group_files = serializers.SerializerMethodField(read_only=True)

    def get_comment_group_files(self, obj):
        serializer = CommentGroupFileSerializer(CommentGroupFile.objects.filter(comment_id=obj.id), many=True,
                                                read_only=True)
        return serializer.data

    class Meta:
        model = CommentGroup
        fields = ['id', 'group_id', 'text', 'comment_group_files', 'user_id', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']


class CommentGroupReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentGroupReply
        fields = ['id', 'user', 'parent_id', 'text', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']


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
        fields = ['id', 'group_id', 'step_id', 'text', 'commented_by', 'date_created', 'date_modified']
        read_only_fields = ['id', 'commented_by', 'step_id', 'date_created', 'date_modified']


class CommentStepReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentStepReply
        fields = ['id', 'user', 'parent_id', 'text', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']
