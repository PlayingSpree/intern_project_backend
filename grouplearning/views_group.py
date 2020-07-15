from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from authapp.serializers import UserDataSerializer
from grouplearning.models import Group, Assignment, CommentGroup, CommentStep, CommentGroupReply, CommentStepReply
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers import GroupSerializer, MemberPostSerializer, CommentGroupSerializer, \
    CommentStepSerializer, CommentGroupReplySerializer, CommentStepReplySerializer
from grouplearning.serializers_assignment import AssignmentSerializer
from grouplearning.serializers_course import GroupCourseSerializer
from sop.serializers import CourseSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    # Multi serializer_classes because Swagger is noob
    serializer_classes = [
        (['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'], GroupSerializer),
        (['member'], UserDataSerializer),
        (['course'], CourseSerializer),
        (['member_post'], MemberPostSerializer),
        (['course_post'], GroupCourseSerializer),
        (['assignment'], AssignmentSerializer),
        (['comment_group'], CommentGroupSerializer),
        (['comment_step'], CommentStepSerializer),
        (['comment_group_reply'], CommentGroupReplySerializer),
        (['comment_step_reply'], CommentStepReplySerializer),
    ]
    permissions = [
        (['list', 'retrieve', 'member', 'course', 'assignment', 'comment_group', 'comment_step', 'comment_group_reply', 'comment_step_reply'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy', 'member_post', 'course_post'], [IsAdminUser])
    ]

    def get_serializer_class(self):
        for p in self.serializer_classes:
            if self.action in p[0]:
                return p[1]
        return GroupSerializer

    def get_permissions(self):
        return get_permissions_multi(self)

    def isingroup(self, request, group):
        if request.user.is_staff:
            return True
        return group.user_joined.filter(id=request.user.id).exists()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True)
    def member(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserDataSerializer(group.user_joined, many=True)
        return Response(serializer.data)

    @member.mapping.post
    def member_post(self, request, pk=None):
        serializer = MemberPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = get_object_or_404(Group.objects.filter(id=pk))
        group.user_joined.clear()
        group.user_joined.add(*serializer.validated_data['new_user_joined_list'])

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def course(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(group.courses, many=True)
        return Response(serializer.data)

    @course.mapping.post
    def course_post(self, request, pk=None):
        serializer = GroupCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = get_object_or_404(Group.objects.filter(id=pk))
        group.courses.clear()
        group.courses.add(*serializer.validated_data['new_course_id_list'])

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def assignment(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssignmentSerializer(Assignment.objects.filter(group_id=pk), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comment_group(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentGroupSerializer(CommentGroup.objects.filter(group_id=pk), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comment_group_reply(self, request, pk=None):
        comment_group = get_object_or_404(CommentGroup.objects.filter(id=pk))
        group = Group.objects.filter(id=comment_group.group_id.id)
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentGroupReplySerializer(CommentGroupReply.objects.filter(parent_id=pk), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comment_step(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentStepSerializer(CommentStep.objects.filter(group_id=pk), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comment_step_reply(self, request, pk=None):
        comment_step = get_object_or_404(CommentStep.objects.filter(id=pk))
        group = Group.objects.filter(id=comment_step.group_id.id)
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentStepReplySerializer(CommentStepReply.objects.filter(parent_id=pk), many=True)
        return Response(serializer.data)
