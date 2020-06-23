from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    grp_creator = UserSerializer(source='creator_id')

    class Meta:
        model = Group
        fields = ['id', 'grp_name', 'grp_description', 'grp_image', 'grp_creator']
        read_only_fields = ['id', 'grp_creator']
        extra_kwargs = {'creator_id': {'write_only: True'}}

