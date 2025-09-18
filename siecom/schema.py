import graphene
from core.graphql import AuthUserMutation, UserQuery, ProductMutation


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthUserMutation, ProductMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
