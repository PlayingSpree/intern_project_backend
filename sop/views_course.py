from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sop.models import Course, Post
from sop.permissions import IsCreatorUser, get_permissions_multi
from sop.serializers import CourseSerializer, CourseCreateSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsCreatorUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)

    def create(self, request, *args, **kwargs):
        serializer = CourseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = Course.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            cover=serializer.validated_data['cover'],
            publish=serializer.validated_data['publish'],
            creator_id=request.user,
        )
        for post in Post.objects.filter(id__in=serializer.validated_data['posts']):
            course.posts.add(post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
