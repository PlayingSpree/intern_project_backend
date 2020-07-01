from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from grouplearning.models import Assignment, AssignmentFile, AssignmentWork, AssignmentWorkFile
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers_assignment import AssignmentSerializer, AssignmentFileSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)

    def get_queryset(self):
        user = self.request.user
        return Assignment.objects.filter(group_id__user_joined=user.id)


class AssignmentFileViewSet(viewsets.ModelViewSet):
    queryset = AssignmentFile.objects.all()
    serializer_class = AssignmentFileSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)


class AssignmentWorkViewSet(viewsets.ModelViewSet):
    queryset = AssignmentWork.objects.all()
    serializer_class = AssignmentSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)


class AssignmentWorkFileViewSet(viewsets.ModelViewSet):
    queryset = AssignmentWorkFile.objects.all()
    serializer_class = AssignmentFileSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)
