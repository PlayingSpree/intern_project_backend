from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAdminUser


def get_permissions_multi(self):
    permission_classes = [IsAdminUser]
    for p in self.permissions:
        if self.action in p[0]:
            permission_classes = p[1]
            break
    return [permission() for permission in permission_classes]
