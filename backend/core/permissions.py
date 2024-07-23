from rest_framework.permissions import BasePermission
from core.models import Guest


class IsAuthenticatedGuest(BasePermission):
    """
    Allows access only to authenticated guest users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and isinstance(request.user, Guest)
        )
