import json
import requests
from unittest import mock
from core.tests.gql_queries import user as user_queries
from core.graphql.user.feedback import UserFeedback


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code=200):
        super().__init__()
        self.status_code = status_code
        self._content = json.dumps(json_data).encode("utf-8")

    def json(self):
        return json.loads(self.text)


@mock.patch("core.utils.auth.requests.get")
def test_auth_user_with_invalid_token(mock_get, unauth_client, invalid_oidc_token):
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
    response = unauth_client.execute(
        user_queries.login_user_mutation(invalid_oidc_token),
    )
    data = response["data"]["loginUser"]
    assert not data["success"]
    assert data["message"] == UserFeedback.INVALID_ACCESS_TOKEN
