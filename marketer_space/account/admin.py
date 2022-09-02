from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .models import Organization, OrganizationAdminUser, AdminUser


@admin.register(Account)
class AccountAdmin(UserAdmin):
    save_as = True
    list_display = ('id', 'organization', 'username', 'role')

    def get_queryset(self, request):
        return Account.objects.filter(role="user")

@admin.register(OrganizationAdminUser)
class OrganizationAdminUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'username', 'role')

    def get_queryset(self, request):
        return OrganizationAdminUser.objects.filter(role='organization_admin')

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'username', 'role')

    def get_queryset(self, request):
        return AdminUser.objects.filter(is_superuser=True)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'domain', 'name', )




# @admin.register(models.CreatorUser)
# class CreatorUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'address', 'username', 'chain', 'is_active', 'nonce', 'action_list', 'last_login')
#     delete_confirmation_template = 'admin/users/delete_user_confirmation.html'
#     list_display_links = ('address', 'username')

