import factory
from factory.django import DjangoModelFactory
from core.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    username = factory.Sequence(lambda n: f"user{n}")
    oidc_subject = factory.Sequence(lambda n: f"subject{n}")
    oidc_issuer = factory.Faker("url")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
