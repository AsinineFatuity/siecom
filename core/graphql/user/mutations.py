import graphene
import traceback
from django.contrib.auth import login, logout
from core.graphql.user.types import UserType
from core.graphql.user.feedback import UserFeedback
from core.models import User
from core.utils.auth import VerifyOidcToken


class LoginUser(graphene.Mutation):
    class Arguments:
        access_token = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)

    def mutate(root, info, access_token):
        try:
            user_info = VerifyOidcToken.verify_token(access_token)
            if not user_info:
                return LoginUser(
                    success=False,
                    message=UserFeedback.INVALID_ACCESS_TOKEN,
                    user=None,
                )
            user = User.objects.filter(
                oidc_subject=user_info.get("sub"),
                oidc_issuer=user_info.get("iss"),
                email=user_info.get("email"),
            ).first()
            if user:
                User.update_existing_user(user, **user_info)
            else:
                user = User.create_new_user(**user_info)
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
        try:
            logout(info.context)
            return LogoutUser(success=True, message=UserFeedback.LOGOUT_SUCCESS)
        except Exception:
            traceback.print_exc()
            return LogoutUser(success=False, message=UserFeedback.LOGOUT_ERROR)


class AuthUserMutation(graphene.ObjectType):
    authenticate_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
