from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from grouplearning.models import Group
from grouplearning.permissions import IsCreatorUser, MultiPermissionMixin
from grouplearning.serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet, MultiPermissionMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    parser_classes = (MultiPartParser,)
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAuthenticated])
    ]

    def get_permissions(self):
        for p in self.permissions:
            if self.action in p[0]:
                permission_classes = p[1]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        if request.user.id == Group.creator_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else: