from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from sop.models import Step
from sop.permissions import IsCreatorUser, MultiPermissionMixin
from sop.serializers import StepSerializer


class StepViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, MultiPermissionMixin):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permissions = [
        (['retrieve', 'file'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsCreatorUser])
    ]
    parser_classes = (MultiPartParser,)
