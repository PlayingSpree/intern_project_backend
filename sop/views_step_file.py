from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from sop.models import StepFile
from sop.permissions import IsAdminUser, get_permissions_multi
from sop.serializers import StepFileSerializer


class StepFileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    queryset = StepFile.objects.all()
    serializer_class = StepFileSerializer
    permissions = [
        (['retrieve'], [IsAuthenticated]),
        (['create', 'destroy'], [IsAdminUser])
    ]

    def get_permissions(self):
        return get_permissions_multi(self)
