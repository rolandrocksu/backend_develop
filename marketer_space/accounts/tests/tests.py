from django.test import TestCase
from django.urls import reverse
from accounts.models import Organization, Account
from requests import Response
import requests
import json
from .factories import OrganizationFactory


class InvitationTestCase(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory(name="Test Organization")
        self.admin_user = Account.objects.create(
            email="admin@gmail.com",
            is_superuser=True,
        )
        self.password = "tester1234"
        self.admin_user.set_password(self.password)
        self.admin_user.save()


        self.data = {
            "organization_id": self.organization.id,
            "email": "new_user@gmail.com",
            "first_name": "User",
            "last_name": "Useryan",
            "status": "user",
        }

    def get_access_token(self):
        url = reverse(
            "token_obtain_pair"
        )
        response = self.client.post(url, data={"email": self.admin_user.email, "password": self.password}, )
        return {
            "access": response.json().get('access'),
            "refresh": response.json().get('refresh')
        }

    def test_super_admin(self):
        url = reverse(
            'account-list'
        )
        tokens = self.get_access_token()
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        response = self.client.get(url, headers=self.heads)
        self.assertEqual(response.status_code, 200)
