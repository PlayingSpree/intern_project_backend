from rest_framework.permissions import BasePermission


class IsCreatorUser(BasePermission):
    """
    Allows access only to creator and admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.sop_isCreator or request.user.is_staff))