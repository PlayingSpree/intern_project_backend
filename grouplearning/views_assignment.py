from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from grouplearning.models import Assignment, AssignmentFile, AssignmentWork, AssignmentWorkFile, Group
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers_assignment import AssignmentSerializer, AssignmentFileSerializer, \
    AssignmentWorkSerializer, AssignmentWorkFileSerializer


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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(admin_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignmentFileViewSet(viewsets.ModelViewSet):
    queryset = AssignmentFile.objects.all()
    serializer_class = AssignmentFileSerializer
    permission_classes = [IsAdminUser]


class AssignmentWorkViewSet(viewsets.GenericViewSet):
    queryset = AssignmentWork.objects.all()
    serializer_class = AssignmentWorkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return AssignmentWork.objects.filter(user_id=user.id)

    def isingroup(self, request, assignment_id):
        # Check if user is in group
        assignment = Assignment.objects.filter(id=assignment_id)
        group = Group.objects.filter(id=assignment[0].group_id.id)
        return group[0].user_joined.filter(id=request.user.id).exists()

    def create(self, request):
        # Locked user
        request.data['user_id'] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if user is in group
        if self.isingroup(request, serializer.validated_data['assignment_id'].id):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if self.isingroup(request, instance.assignment_id.id):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignmentWorkFileViewSet(viewsets.ModelViewSet):
    queryset = AssignmentWorkFile.objects.all()
    serializer_class = AssignmentWorkFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return AssignmentWorkFile.objects.filter(assignment_work_id__user_id=user.id)
