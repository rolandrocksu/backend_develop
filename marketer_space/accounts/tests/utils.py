from django.urls import reverse
from accounts.models import Organization, Account
import requests


def get_access_token(self, username, password):
    url = reverse(
        "token_obtain_pair"
    )
    response = self.client.post(url, data={"email": username, "password": password})
    return {
        "access": response.json().get('access'),
        "refresh": response.json().get('refresh')
    }


def create_user(email, is_superuser, is_org_admin, password, organization):
    user = Account.objects.create(
        email=email,
        is_superuser=is_superuser,
        is_org_admin=is_org_admin,
        organization=organization,
        first_name="Admin",
        last_name="Admin"
    )
    user.set_password(password)
    user.save()

    return user
