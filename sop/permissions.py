from rest_framework.permissions import BasePermission, IsAdminUser


class IsCreatorUser(BasePermission):
    """
    Allows access only to creator and admin users.
    """

    def has_permission(self, request, view):
        if (request.user):
            return bool(request.user.sop_is_creator or request.user.is_staff)
        else:
            return False


class MultiPermissionMixin:
    def get_permissions(self):
        for p in self.permissions:
            print(self.action)
            if self.action in p[0]:
                permission_classes = p[1]
            else:
                permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
