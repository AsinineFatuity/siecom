import graphene
import traceback
from django.contrib.auth import login, logout
from core.graphql.user.types import UserType
from core.graphql.user.feedback import UserFeedback
from core.models import User
from core.utils.auth import OidcTokenVerifier


class LoginUser(graphene.Mutation):
    class Arguments:
        oidc_access_token = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(root, info, oidc_access_token):
        try:
            verifier = OidcTokenVerifier(oidc_access_token)
            user_info = verifier.verify_token()
            if not user_info:
                return LoginUser(
                    success=False,
                    message=UserFeedback.INVALID_ACCESS_TOKEN,
                    user=None,
                )
            user = User.create_or_update_user(**user_info)
            login(info.context, user)

            return LoginUser(
                success=True,
                message=UserFeedback.AUTHENTICATION_SUCCESS,
                user=user,
            )
        except Exception:
            traceback.print_exc()
            return LoginUser(
                success=False,
                message=UserFeedback.AUTHENTICATION_ERROR,
                user=None,
            )


class LogoutUser(graphene.Mutation):
    success = graphene.Boolean(default_value=False)
    message = graphene.String(default_value="")

    def mutate(root, info):
        success = False
        message = UserFeedback.LOGOUT_ERROR
        try:
            logout(info.context)
            success = True
            message = UserFeedback.LOGOUT_SUCCESS
        except Exception:
            traceback.print_exc()
        return LogoutUser(success=success, message=message)


class AuthUserMutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
