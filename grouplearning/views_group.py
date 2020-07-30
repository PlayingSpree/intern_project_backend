from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from authapp.serializers import UserDataSerializer
from grouplearning.filter import MultiSearchFilter
from grouplearning.models import Group, Assignment, CommentGroup, CommentStep, CommentGroupReply, CommentStepReply, \
    CommentGroupFile
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers import GroupSerializer, MemberPostSerializer, CommentGroupSerializer, \
    CommentStepSerializer, CommentGroupReplySerializer, CommentStepReplySerializer, CommentGroupFileWithDateSerializer
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
        (['attachment'], CommentGroupFileWithDateSerializer),
    ]
    permissions = [
        (['list', 'retrieve', 'member', 'course', 'assignment', 'comment_group', 'comment_step', 'comment_group_reply',
          'comment_step_reply', 'attachment'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy', 'member_post', 'course_post'], [IsAdminUser])
    ]
    filter_backends = [MultiSearchFilter]
    search_fields = [(['list'], ['group_name']),
                     (['course'], ['name']),
                     (['assignment'], ['name'])]

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

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.get_queryset()
        else:
            queryset = Group.objects.filter(user_joined=request.user)
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True)
    def member(self, request, pk=None):
        """
        Can use /?idonly to return only the user_id of member.
        """
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        # query_params
        queryset = group.user_joined.all()
        if self.request.query_params.get('idonly', None) is None:
            serializer = UserDataSerializer(queryset, many=True, context={'request': request})
        else:
            return Response(list(queryset.values_list("id", flat=True)))
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
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(self.filter_queryset(group.courses), many=True, context={'request': request})
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
        serializer = AssignmentSerializer(self.filter_queryset(Assignment.objects.filter(group_id=pk)), many=True,
                                          context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def comment_group(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentGroupSerializer(CommentGroup.objects.filter(group_id=pk), many=True,
                                            context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def comment_group_reply(self, request, pk=None):
        comment_group = get_object_or_404(CommentGroup.objects.filter(id=pk))
        group = get_object_or_404(Group.objects.filter(id=comment_group.group_id.id))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentGroupReplySerializer(CommentGroupReply.objects.filter(parent_id=pk), many=True,
                                                 context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def comment_step(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentStepSerializer(CommentStep.objects.filter(group_id=pk), many=True,
                                           context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def comment_step_reply(self, request, pk=None):
        comment_step = get_object_or_404(CommentStep.objects.filter(id=pk))
        group = get_object_or_404(Group.objects.filter(id=comment_step.group_id.id))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentStepReplySerializer(CommentStepReply.objects.filter(parent_id=pk), many=True,
                                                context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def attachment(self, request, pk=None):
        group = get_object_or_404(Group.objects.filter(id=pk))
        # Check if user is in group
        if not self.isingroup(request, group):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentGroupFileWithDateSerializer(CommentGroupFile.objects.filter(comment_id__group_id=pk),
                                                        many=True, context={'request': request})
        return Response(serializer.data)
