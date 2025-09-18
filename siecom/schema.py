import graphene
from core.graphql import AuthUserMutation, UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthUserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
