from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser

from authapp.models import User
from authapp.serializers import UserDataSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permissions = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['email','first_name','last_name']