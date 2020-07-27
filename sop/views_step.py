from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from sop.models import Step ,SopHistory , Session
from sop.permissions import IsAdminUser, get_permissions_multi
from sop.serializers import StepSerializer
from rest_framework.response import Response

class StepViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permissions = [
        (['retrieve', 'file'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsAdminUser])
    ]
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        return get_permissions_multi(self)
