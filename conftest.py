import pytest
from graphene.test import Client
from siecom.schema import schema
from core.tests.factory import UserFactory
from core.models import User


class TestContext:
    def __init__(self, user: User):
        self.user = user


@pytest.fixture
def auth_client(db, user):
    """
    Fixture to create an authenticated GraphQL client.
    """
    user = UserFactory.create()
    context_value = TestContext(user)
    auth_client = Client(schema, context_value=context_value)
    return auth_client


@pytest.fixture
def unauth_client():
    """
    Fixture to create an unauthenticated GraphQL client.
    """
    return Client(schema, context_value=None)


@pytest.fixture(autouse=True)
def mock_oidc_env_vars(monkeypatch):
    """
    Fixture to mock OIDC environment variables.
    """
    monkeypatch.setenv("OIDC_ISSUER", "https://dev-xyz123.us.auth0.com")
    monkeypatch.setenv("OIDC_AUDIENCE", "https://dev-xyz123.us.auth0.com/api/v2/")
    yield
