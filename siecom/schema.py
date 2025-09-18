import graphene
from core.graphql import AuthUserMutation, UserQuery, ProductMutation, ProductQuery


class Query(UserQuery, ProductQuery, graphene.ObjectType):
    pass


class Mutation(AuthUserMutation, ProductMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
