from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from grouplearning.models import CommentGroup, CommentGroupFile, CommentGroupReply, Group
from grouplearning.serializers import CommentGroupSerializer, CommentGroupFileSerializer, CommentGroupReplySerializer


class CommentGroupViewSet(viewsets.ModelViewSet):
    queryset = CommentGroup.objects.all()
    serializer_class = CommentGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CommentGroup.objects.filter(group_id__user_joined=user.id)


class CommentGroupFileViewSet(viewsets.ModelViewSet):
    queryset = CommentGroupFile.objects.all()
    serializer_class = CommentGroupFileSerializer
    permission_classes = [IsAuthenticated]


class CommentGroupReplyViewSet(viewsets.GenericViewSet):
    queryset = CommentGroupReply.objects.all()
    serializer_class = CommentGroupReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CommentGroupReply.objects.filter(user_id=user.id)

    #not really sure about parameter that parent_id
    def isingroup(self, request, parent_id):
        comment_group = CommentGroup.objects.filter(id=parent_id)
        group = Group.objects.filter(id=comment_group[0].group_id.id)
        return group[0].user_joined.filter(id=request.user.id).exists()

    def create(self, request):
        request.data['user_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if user is in group
        #.id again because it is foreignkey? need to get id from parent_id's table?
        if self.isingroup(request, serializer.validated_data['parent_id'].id):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if self.isingroup(request, instance.parent_id.id):
            return Response({"detail": "User not in the group."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


