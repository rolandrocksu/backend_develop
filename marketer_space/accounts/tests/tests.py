from django.test import TestCase
from django.urls import reverse
from accounts.models import Organization, Account
from .utils import get_access_token, create_user
import requests
from .factories import OrganizationFactory, AccountFactory


class AccountsTest(TestCase):
    def setUp(self):
        self.localhost = "http://127.0.0.1:8000"

        self.organization = OrganizationFactory(name="Test Organization")
        self.password = "tester1234"
        self.admin_user = create_user(email="superadmin@gmail.com",
                                      is_superuser=True,
                                      is_org_admin=False,
                                      password=self.password,
                                      organization=self.organization
                                      )
        self.org_admin = create_user(email="orgadmin@gmail.com",
                                     is_superuser=False,
                                     is_org_admin=True,
                                     password=self.password,
                                     organization=self.organization
                                     )
        self.org_user = create_user(email="orguser@gmail.com",
                                    is_superuser=False,
                                    is_org_admin=False,
                                    password=self.password,
                                    organization=self.organization
                                    )

    def test_super_admin_can_access_account_list(self):
        url = reverse(
            'account-list'
        )
        tokens = get_access_token(self, self.admin_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        response = self.client.get(url, headers=self.heads)
        print(response.content)
        print(response.status_code)
        self.assertEqual(res.status_code, 200)

    def test_org_admin_can_access_account_list(self):
        url = reverse(
            'account-list'
        )
        tokens = get_access_token(self, self.org_admin.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 200)

    def test_org_user_cant_access_account_list(self):
        url = reverse(
            'account-list'
        )
        tokens = get_access_token(self, self.org_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 403)

    def test_org_user_can_access_account_details(self):
        url = reverse(
            'account-detail',
            kwargs={
                "pk": self.org_user.id
            }
        )
        tokens = get_access_token(self, self.org_admin.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 200)


class OrganizationTest(TestCase):

    def setUp(self):
        self.localhost = "http://127.0.0.1:8000"

        self.organization = OrganizationFactory(name="Test Organization")
        self.password = "tester1234"
        self.admin_user = create_user(email="superadmin@gmail.com",
                                      is_superuser=True,
                                      is_org_admin=False,
                                      password=self.password,
                                      organization=self.organization
                                      )
        self.org_admin = create_user(email="orgadmin@gmail.com",
                                     is_superuser=False,
                                     is_org_admin=True,
                                     password=self.password,
                                     organization=self.organization
                                     )
        self.org_user = create_user(email="orguser@gmail.com",
                                    is_superuser=False,
                                    is_org_admin=False,
                                    password=self.password,
                                    organization=self.organization
                                    )

    def test_super_admin_can_access_organization_list(self):
        url = reverse(
            'organization-list'
        )
        tokens = get_access_token(self, self.admin_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        # self.client.login(username=self.admin_user.email, password=self.password)
        # response = self.client.post(url, headers=self.heads)
        self.assertEqual(res.status_code, 200)

    def test_org_admin_cant_access_organization_list(self):
        url = reverse(
            'organization-list'
        )
        tokens = get_access_token(self, self.org_admin.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 403)

    def test_org_admin_can_access_organization_detail_view(self):
        url = reverse(
            'organization-detail',
            kwargs={
                "pk": self.organization.id
            }

        )
        tokens = get_access_token(self, self.org_admin.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 200)

    def test_org_user_cant_access_organization_detail_view(self):
        url = reverse(
            'organization-detail',
            kwargs={
                "pk": self.organization.id
            }

        )
        tokens = get_access_token(self, self.org_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 403)

    def test_org_user_cant_access_organization_list(self):
        url = reverse(
            'organization-list'
        )
        tokens = get_access_token(self, self.org_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        res = requests.get(f'{self.localhost}{url}', headers=self.heads)
        self.assertEqual(res.status_code, 403)


class InvitationSendTestCase(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory(name="Test Organization")
        self.admin_user = Account.objects.create(
            email="admin@gmail.com",
            is_superuser=True,
            first_name="Admin",
            last_name="Admin"
        )
        self.password = "tester1234"
        self.admin_user.set_password(self.password)
        self.admin_user.save()

        self.data = {
            "organization_id": self.organization.id,
            "email": "new_user@gmail.com",
            "first_name": "User",
            "last_name": "Useryan",
            "receiver": "new_user@gmail.com",
            "status": "user",
        }

    def test_super_admin_can_send_invitation_mail(self):
        url = reverse(
            'invitation-mail'
        )
        tokens = get_access_token(self, self.admin_user.email, self.password)
        self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
        response = requests.post(f'http://127.0.0.1:8000{url}', data=self.data, headers=self.heads)
        self.assertEqual(response.status_code, 200)

    # def test_org_admin_can_send_invitation_mail(self):
    #     url = reverse(
    #         'invitation-mail'
    #     )
    #     tokens = get_access_token(self, self.admin_user.email, self.password)
    #     self.heads = {'Authorization': f"Bearer {tokens.get('access')}"}
    #     response = requests.post(f'http://127.0.0.1:8000{url}', data=self.data, headers=self.heads)
    #     print(response.content)
    #     self.assertEqual(response.status_code, 200)


class InvitedUserCreationTest(TestCase):
    pass
