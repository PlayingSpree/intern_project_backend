from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from sop.models import StepFile
from sop.permissions import IsCreatorUser, MultiPermissionMixin
from sop.serializers import StepFileSerializer


class StepFileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, MultiPermissionMixin):
    queryset = StepFile.objects.all()
    serializer_class = StepFileSerializer
    permissions = [
        (['retrieve'], [IsAuthenticated]),
        (['create', 'destroy'], [IsCreatorUser])
    ]
    parser_classes = (MultiPartParser,)
