from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group, CommentGroup, CommentGroupFile, CommentGroupReply


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
        read_only_fields = ['id', 'comment_id']


class CommentGroupSerializer(serializers.ModelSerializer):
    commentator = UserSerializer(source='user_id', read_only=True)
    comment_group_file = CommentGroupFileSerializer()

    class Meta:
        model = CommentGroup
        fields = ['id', 'group_id', 'text', 'comment_group_file', 'commentator']
        read_only_fields = ['id', 'commentator']

    def create(self, validated_data):
        comment_group_file_data = validated_data.pop('comment_group_file')
        CommentGroup_model = CommentGroup.objects.create(**validated_data)
        CommentGroupFile.objects.create(CommentGroup_model=CommentGroup_model, **comment_group_file_data)
        return CommentGroup_model


class CommentGroupReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGroupReply
        fields = ['id', 'user_id', 'parent_id']


class AddUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'user_joined']

    def update(self, instance, validated_data):
        user_id = validated_data.pop('user_joined')
        user_joined = Group.objects.create(**user_id)

        return user_joined

