from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from grouplearning.models import CommentGroup
from grouplearning.permissions import get_permissions_multi
from grouplearning.serializers import CommentGroupSerializer


class CommentGroupViewSet(viewsets.ModelViewSet):
    queryset = CommentGroup.objects.all()
    serializer_class = CommentGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

