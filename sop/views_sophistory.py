from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from sop.models import SopHistory
from sop.serializers import SopHistorySerializer


class SopHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SopHistory.objects.all()
    serializer_class = SopHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SopHistory.objects.filter(user_id=user)
