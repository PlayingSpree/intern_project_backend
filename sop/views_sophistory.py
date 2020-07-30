from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from sop.models import SopHistory
from sop.permissions import get_permissions_multi
from sop.serializers import SopHistorySerializer


class SopHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SopHistory.objects.all()
    serializer_class = SopHistorySerializer
    permissions = [
        (['retrieve'], [IsAuthenticated]),
        (['create', 'destroy'], [IsAdminUser])
    ]
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        return get_permissions_multi(self)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
