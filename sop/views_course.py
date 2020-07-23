from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from sop.models import Course
from sop.permissions import get_permissions_multi
from sop.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            return Course.objects.filter(publish=True)

    def get_permissions(self):
        return get_permissions_multi(self)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
