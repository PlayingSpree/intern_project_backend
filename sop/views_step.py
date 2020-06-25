from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from sop.models import Step, StepFile
from sop.permissions import IsCreatorUser, MultiPermissionMixin
from sop.serializers import StepSerializer, StepFileSerializer


class StepViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, MultiPermissionMixin):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permissions = [
        (['retrieve', 'file'], [IsAuthenticated]),
        (['create', 'update', 'partial_update', 'destroy'], [IsCreatorUser])
    ]
    parser_classes = (MultiPartParser,)

    @action(detail=True,url_path='file', url_name='file-list')
    def file_list(self, request, pk=None):
        instance = get_object_or_404(StepFile.objects.filter(step_id=pk))
        serializer = StepFileSerializer(instance, many=True)
        return Response(serializer.data)
