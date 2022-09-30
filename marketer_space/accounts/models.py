from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone


class Organization(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    domain = models.CharField(max_length=256)
    name = models.CharField(max_length=128)


class Account(AbstractUser):
    username = None

    email = models.EmailField("Email", unique=True)
    country = models.CharField(max_length=128)
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True, related_name='users'
    )
    profile_picture = models.ImageField(upload_to='profile/%Y/%m/%d', null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['organization']

    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


class Invitation(models.Model):
    invitor = models.EmailField(max_length=100)
    receiver = models.EmailField(max_length=100)
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True
    )
    status = models.CharField(max_length=50)
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

# class SuperAdminUser(Account):
#     class Meta:
#         proxy = True
#         verbose_name = 'Admin user'
#         verbose_name_plural = 'Admin Users'
#
#
# class OrganizationAdminUser(Account):
#     class Meta:
#         proxy = True
#         verbose_name = 'Organization Admin'
#         verbose_name_plural = 'Organization Admin'
#
