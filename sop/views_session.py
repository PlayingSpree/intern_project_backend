from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sop.models import Session, SopHistory , Step
from sop.permissions import IsAdminUser, get_permissions_multi
from sop.serializers import SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permissions = [
        (['list', 'retrieve'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        return get_permissions_multi(self)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Session.objects.all()
        else:
            return Session.objects.filter(publish=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        SopHistory.push(request.user, instance)
        return Response(serializer.data)