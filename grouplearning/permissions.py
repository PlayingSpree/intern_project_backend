from rest_framework.permissions import BasePermission, IsAdminUser


class IsCreatorUser(BasePermission):
    """
    Allows access only to creator and admin users.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return bool(request.user.sop_is_creator or request.user.is_staff)
        else:
            return False


def get_permissions_multi(self):
    for p in self.permissions:
        print(self.action)
        if self.action in p[0]:
            permission_classes = p[1]
            print(permission_classes)
        else:
            permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]
