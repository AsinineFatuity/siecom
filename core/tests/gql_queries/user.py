def login_user_mutation(oidc_access_token: str):
    return (
        """
    mutation {
        loginUser(oidcAccessToken: "%s") {
            success
            message
            user {
                id
                email
                firstName
                lastName
            }
        }
    }
    """
        % oidc_access_token
    )
