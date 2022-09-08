from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return False
        elif request.user.is_superuser:
            return True
        else:
            return False


class IsOrganizationAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return False
        elif request.user.is_org_admin:
            return True
        else:
            return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return False
        elif not request.user.is_superuser and not request.user.is_org_admin:
            return True
        else:
            return False
