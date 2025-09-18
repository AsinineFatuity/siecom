import pytest
from graphene.test import Client
from django.test.client import RequestFactory
from siecom.schema import schema
from core.tests.factory import UserFactory
from core.tests.utils import make_oidc_token
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
    request_factory = RequestFactory()
    request = request_factory.post("/graphql/")
    return Client(schema, context_value=request)


@pytest.fixture(autouse=True)
def mock_oidc_env_vars(monkeypatch):
    """
    Fixture to mock OIDC environment variables.
    """
    monkeypatch.setenv("OIDC_ISSUER", "https://dev-xyz123.us.auth0.com")
    monkeypatch.setenv("OIDC_AUDIENCE", "https://dev-xyz123.us.auth0.com/api/v2/")
    yield


@pytest.fixture
def valid_oidc_token():
    """
    Fixture to provide a valid OIDC access token for testing.
    """
    return make_oidc_token()


@pytest.fixture
def invalid_oidc_token():
    """
    Fixture to provide an invalid OIDC access token for testing.
    """
    return make_oidc_token(exp_minutes=-5)
