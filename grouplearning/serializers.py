from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group


# create group
class GroupSerializer(serializers.ModelSerializer):
    group_creator = UserSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_description', 'default_course', 'group_image', 'group_creator']
        read_only_fields = ['id', 'group_creator']


