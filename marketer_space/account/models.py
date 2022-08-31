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
        'Organization', on_delete=models.SET_NULL, null=True, blank=True
    )

    profile_picture = models.ImageField(upload_to='profile/%Y/%m')
    role = models.CharField(
        max_length=45,
        choices=ACCOUNT_TYPE,
        default=ACCOUNT_TYPE[2]
    )

    creation_date = models.DateTimeField(auto_now=True)
    modification_date = models.DateTimeField(null=True)


class Organization(models.Model):
    domain = models.CharField(max_length=256)
    name = models.CharField(max_length=128)

