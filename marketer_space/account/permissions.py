from rest_framework import permissions

from .models import Account


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == Account.ACCOUNT_TYPE[0]:
            return True
        return False


class OrganizationPermission(permissions.BasePermission):
    organization_admin_methods = ("PUT", "PATCH", "GET")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True

        if (request.user.role == 'organization_admin' and
                request.method in self.organization_admin_methods):
            return True
        if (
                request.method == 'GET' and request.user.organization and
                view.kwargs.get('organization_pk') in request.user.organization
        ):
            return True
        return False


class InviteUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True

        if (
                request.user.role == 'organization_admin' and
                request.user.organization and
                request.data.get('organization_id') in
                request.user.organization
        ):
            return True

        return False
