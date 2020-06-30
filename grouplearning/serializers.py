from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group, Role, UserRole


# create group
class GroupSerializer(serializers.ModelSerializer):
    group_creator = UserSerializer(source='creator_id', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_description', 'group_image', 'group_creator']
        read_only_fields = ['id', 'group_creator']


class CreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name']


class AddRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['user_id', 'group_id', 'role_id']
