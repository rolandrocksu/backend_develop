from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from .models import Account, Organization
from .serializers import (
    MyTokenObtainPairSerializer,
    AccountSerializer,
    OrganizationSerializer)

from .mixin import PermissionPolicyMixin
from .permissions import (
    IsSuperAdmin,
    IsOrganizationAdmin,
    IsUser
)

class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer
    queryset = Account.objects.none()
    # permission_classes = [AllowAny]
    permission_classes_per_method = {
        "list" : [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "retrieve": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "create": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "update": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "partial_update": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "destroy": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Account.objects.none()
        elif user.is_superuser:
            return Account.objects.all()
        elif user.is_org_admin:
            return Account.objects.filter(organization=user.organization)
        else:
            return Account.objects.filter(id=user.id)


class OrganizationViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.none()
    permission_classes_per_method = {
        "list" : [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "retrieve": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "create": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "update": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "partial_update": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
        "destroy": [IsUser | IsOrganizationAdmin | IsSuperAdmin | IsAdminUser],
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Organization.objects.none()
        elif user.is_superuser:
            return Organization.objects.all()
        else:
            return Organization.objects.filter(id=user.organization.id)





class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

