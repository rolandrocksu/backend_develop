from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    ACCOUNT_TYPE = (
        ('super_admin', 'Super Admin'),
        ('organization_admin', 'Organization Admin'),
        ('user', 'User')
    )

    country = models.CharField(max_length=128)
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=False
    )

    profile_picture = models.ImageField(upload_to='profile/%Y/%m')
    role = models.CharField(
        max_length=45,
        choices=ACCOUNT_TYPE,
        default=ACCOUNT_TYPE[2],
        null=False
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)


class AdminUser(Account):
    class Meta:
        proxy = True
        verbose_name = 'Admin user'
        verbose_name_plural = 'Admin Users'


class OrganizationAdminUser(Account):
    class Meta:
        proxy = True
        verbose_name = 'Organization Admin'
        verbose_name_plural = 'Organization Admin'


class Organization(models.Model):
    domain = models.CharField(max_length=256)
    name = models.CharField(max_length=128)

