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

    def create(self, request, *args, **kwargs):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.filter(id=serializer.validated_data['id'])
        if group:
            for user_joined in serializer.validated_data['user_joined']:
                group[0].user_joined.add(user_joined)
        else:
            NotFound

        return Response(serializer.data, status=status.HTTP_201_CREATED)
