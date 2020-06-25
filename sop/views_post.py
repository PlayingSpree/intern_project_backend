from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sop.models import Post
from sop.permissions import IsCreatorUser, MultiPermissionMixin
from sop.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet, MultiPermissionMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsCreatorUser])
    ]
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)