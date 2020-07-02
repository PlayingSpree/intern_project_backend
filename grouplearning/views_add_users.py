from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from grouplearning.models import Group
from grouplearning.serializers import AddUserSerializer


class AddUserViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Group.objects.create(
            id=serializer.validated_data['id'],
        )
        if Group.objects.filter(group_id=serializer.validated_data['id'].id):
            for user_joined in Group.objects.filter(id__in=serializer.validated_data['user_joined']):
                user.user_joined.add(user_joined)
        else:
            NotFound

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
