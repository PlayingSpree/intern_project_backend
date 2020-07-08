from djoser.serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from grouplearning.models import Group


class GetMemberViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        serializer = UserSerializer(group.user_joined, many=True)
        return Response(serializer.data)
