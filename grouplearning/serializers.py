import os

from rest_framework import serializers

from django.contrib.auth import get_user_model

from authapp.serializers import UserDataSerializer
from .models import Group, CommentGroup, CommentGroupFile, CommentGroupReply, CommentStep, CommentStepReply

User = get_user_model()


# create group
class GroupSerializer(serializers.ModelSerializer):
    group_creator = UserDataSerializer(source='creator_id', read_only=True)
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        file = {
            "url": representation.pop("file"),
            "size": instance.file.size,
            "name": os.path.basename(instance.file.name),
        }
        representation['file'] = file
        return representation


class CommentGroupFileWithDateSerializer(serializers.ModelSerializer):
    date_modified = serializers.SerializerMethodField(read_only=True)

    def get_date_modified(self, obj):
        return CommentGroup.objects.filter(pk=obj.comment_id.id)[0].date_modified

    class Meta:
        model = CommentGroupFile
        fields = ['id', 'comment_id', 'file', 'date_modified']
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
    user = UserDataSerializer(source='user_id', read_only=True)

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

    class Meta:
        model = CommentStep
        fields = ['id', 'group_id', 'step_id', 'text', 'user_id', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']



class CommentStepReplySerializer(serializers.ModelSerializer):
    user = UserDataSerializer(source='user_id', read_only=True)

    class Meta:
        model = CommentStepReply
        fields = ['id', 'user', 'parent_id', 'text', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']


def valid_user_and_not_admin(user_id):
    user = User.objects.filter(pk=user_id)
    if not user.exists():
        raise serializers.ValidationError("{0} is not a valid User id.".format(user_id))
    return not user[0].is_staff


class MemberPostSerializer(serializers.Serializer):
    new_user_joined_list = serializers.ListField(child=serializers.IntegerField())

    def validate_new_user_joined_list(self, value):
        return [x for x in value if valid_user_and_not_admin(x)]
