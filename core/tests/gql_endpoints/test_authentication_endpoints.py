import json
import requests
from unittest import mock
from core.tests.gql_queries import user as user_queries
from core.graphql.user.feedback import UserFeedback
from core.models import User


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code=200):
        super().__init__()
        self.status_code = status_code
        self._content = json.dumps(json_data).encode("utf-8")

    def json(self):
        return json.loads(self.text)


@mock.patch("core.utils.auth.requests.get")
def test_auth_user_with_invalid_token(
    mock_get, unauthenticated_client, invalid_oidc_token
):
    """
    Test authentication with an invalid OIDC access token.
    """
    mocked_response = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "valid_kid",
                "use": "sig",
                "n": "valid_n",
                "e": "AQAB",
            }
        ]
    }
    mock_get.return_value = MockResponse(mocked_response)
    response = unauthenticated_client.execute(
        user_queries.login_user_mutation(invalid_oidc_token),
    )
    assert "errors" not in response
    data = response["data"]["loginUser"]
    assert not data["success"]
    assert data["message"] == UserFeedback.INVALID_ACCESS_TOKEN


@mock.patch("core.utils.auth.requests.get")
@mock.patch("core.utils.auth.jwt.get_unverified_header")
@mock.patch("core.utils.auth.jwt.decode")
@mock.patch("core.utils.auth.OidcTokenVerifier._request_user_info_from_oidc_provider")
def test_auth_user_with_valid_token(
    mock_request_user_info,
    mock_decode,
    mock_get_unverified_header,
    mock_get,
    unauthenticated_client,
    valid_oidc_token,
    db,
):
    """
    Test authentication with a valid OIDC access token.
    """
    response_dict = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "valid_kid",
                "use": "sig",
                "n": "valid_n",
                "e": "AQAB",
            }
        ]
    }
    mock_get_unverified_header.return_value = response_dict["keys"][0]
    mock_get.return_value = MockResponse(response_dict)
    mock_decode.return_value = {
        "sub": "google-oauth2|116335214551149049094",
        "email": "test@yopmail.com",
        "iat": 1742339743,
        "exp": 1742426143,
        "iss": "https://dev-xyz123.us.auth0.com/",
        "aud": [
            "https://dev-xyz123.us.auth0.com/api/v2/",
            "https://dev-xyz123.us.auth0.com/userinfo",
        ],
        "scope": "openid profile email",
    }
    mock_request_user_info.return_value = {
        "sub": "google-oauth2|116335214551149049094",
        "email": "test@yopmail.com",
        "given_name": "Test",
        "family_name": "User",
    }
    response = unauthenticated_client.execute(
        user_queries.login_user_mutation(valid_oidc_token),
    )
    assert "errors" not in response
    data = response["data"]["loginUser"]
    assert data["success"]
    assert data["message"] == UserFeedback.AUTHENTICATION_SUCCESS
    assert data["user"] is not None
    user_info = data["user"]
    assert user_info["email"] == "test@yopmail.com"
    assert user_info["firstName"] == "Test"
    assert user_info["lastName"] == "User"
    assert user_info["id"] is not None
    user = User.objects.filter(email="test@yopmail.com").first()
    assert user is not None
