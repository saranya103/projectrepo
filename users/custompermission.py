
from rest_framework import permissions


class Isadmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff and request.user.is_superuser:
            return True
