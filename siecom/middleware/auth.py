import logging
import traceback
from django.contrib.auth.models import AnonymousUser
from graphql import GraphQLResolveInfo
from core.utils.auth import OidcTokenVerifier
from core.models import User


class OIDCAuthenticationMiddleware:
    def resolve(self, next, root, info: GraphQLResolveInfo, **kwargs):
        request = info.context
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            request.user = AnonymousUser()
            return next(root, info, **kwargs)

        token = auth_header.split(" ")[1]
        try:
            verifier = OidcTokenVerifier()
            user_info = verifier.verify_token(token)
            if not user_info:
                request.user = AnonymousUser()
                return next(root, info, **kwargs)
            user = User.create_or_update_user(**user_info)
            request.user = user
        except Exception:
            traceback.print_exc()
            logging.error(f"{__name__}: Error during OIDC authentication")
            request.user = AnonymousUser()

        return next(root, info, **kwargs)
