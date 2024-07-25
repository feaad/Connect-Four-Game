from core.permissions import IsAuthenticatedGuest
from rest_framework.permissions import IsAuthenticated


class PermissionMixin:
    def get_permissions(self):
        user = self.request.user
        if hasattr(user, "guest_id"):
            return [IsAuthenticatedGuest()]
        else:
            return [IsAuthenticated()]
