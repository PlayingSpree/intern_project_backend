
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from grouplearning.models import Group
from grouplearning.serializers import AddUserSerializer


class AmountPartialUpdateView(APIView):

    def patch(self, request, pk, user_id):
        # if no model exists by this PK, raise a 404 error
        model = get_object_or_404(Group, pk=pk)
        # this is the only field we want to update
        data = {"user_joined": Group.user_joined}
        serializer = AddUserSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

