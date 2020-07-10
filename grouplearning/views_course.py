from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from grouplearning.models import Group
from grouplearning.serializers_course import GroupCourseSerializer
from sop.serializers import CourseSerializer


class GroupCourseViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupCourseSerializer
    permissions = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group.objects.filter(serializer.validated_data['group_id']))
        group.courses.clear()
        group.courses.add(*serializer.validated_data['new_course_id_list'])
        return Response(serializer.data, status=status.HTTP_200_OK)
