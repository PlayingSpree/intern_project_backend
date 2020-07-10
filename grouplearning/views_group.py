from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from authapp.serializers import UserDataSerializer
from grouplearning.models import Group
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers import GroupSerializer
from sop.serializers import CourseSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permissions = [
        (['list', 'retrieve', 'member', 'course'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        return get_permissions_multi(self)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True)
    def member(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        serializer = UserDataSerializer(group.user_joined, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def course(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        serializer = CourseSerializer(group.courses, many=True)
        return Response(serializer.data)
