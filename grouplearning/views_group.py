from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from grouplearning.models import Group
from grouplearning.serializers import GroupSerializer


class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

