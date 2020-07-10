from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from grouplearning.models import Group
from grouplearning.serializers import AddUserSerializer


class AddUserViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = AddUserSerializer
    permission_classes = [IsAdminUser]

    def isingroup(self, request, group_id, user_id):
        group = Group.objects.filter(id=group_id)
        return group[0].user_joined.filter(id=user_id).exists()

    def create(self, request, *args, **kwargs):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = Group.objects.filter(id=serializer.validated_data['id'])
        if group:
            if not self.isingroup(request, serializer.validated_data['id'], serializer.validated_data['id']):
                for user_joined in serializer.validated_data['user_joined']:
                    group[0].user_joined.add(user_joined)

            elif self.isingroup(request, serializer.validated_data['id']):
                return Response({"detail": "This user has already joined the group."}, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({"detail": "please, check the GroupID again."}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
