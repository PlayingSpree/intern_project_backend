from rest_framework.permissions import BasePermission


class IsCreatorUser(BasePermission):
    """
    Allows access only to creator and admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.group_learning_is_creator or request.user.is_staff))