import factory.django as djangofactory
from accounts.models import Organization, Account


class OrganizationFactory(djangofactory.DjangoModelFactory):

    class Meta:
        model = Organization
        django_get_or_create = ["name"]

class AccountAdminFactory(djangofactory.DjangoModelFactory):

    class Meta:
        model = Account
        django_get_or_create = ["role"]
