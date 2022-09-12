import factory.django as djangofactory
from accounts.models import Organization, Account


class OrganizationFactory(djangofactory.DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ["name"]


class AccountFactory(djangofactory.DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ["email", "is_superuser", "is_org_admin", "password"]
