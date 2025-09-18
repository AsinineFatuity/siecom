from core.tests.gql_queries import user as user_queries
from core.graphql.user.feedback import UserFeedback


def test_auth_user_with_invalid_token(unauth_client):
    """
    Test authentication with an invalid OIDC access token.
    """
    response = unauth_client.execute(
        user_queries.login_user_mutation("invalid_token"),
    )
    data = response["data"]["loginUser"]
    assert not data["success"]
    assert data["message"] == UserFeedback.INVALID_ACCESS_TOKEN
