from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name' )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'organization', 'first_name', 'last_name',
                  'country', 'profile_picture', 'password',)

    def get_queryset(self, request):
        return Account.objects.all()

# @admin.register(OrganizationAdminUser)
# class OrganizationAdminUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'organization')
#
#     def get_queryset(self, request):
#         return Account.objects.filter(is_org_admin=True)
#
# @admin.register(SuperAdminUser)
# class AdminUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'organization')
#
#     def get_queryset(self, request):
#         return Account.objects.filter(is_super_admin=True)

