from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from sop.models import Post
from sop.serializers import PostSerializer


class PostViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

