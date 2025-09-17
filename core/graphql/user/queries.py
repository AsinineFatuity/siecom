import graphene
from core.graphql.user.types import UserType
from siecom.decorators import logged_in_user_required


class UserQuery:
    user_details = graphene.Field(UserType)

    @logged_in_user_required
    def resolve_user_details(root, info):
        return info.context.user
