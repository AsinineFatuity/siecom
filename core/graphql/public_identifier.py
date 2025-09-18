from graphene_django.types import DjangoObjectType


class CustomDjangoObjectType(DjangoObjectType):
    def resolve_id(root, info):
        return root.public_id

    def resolve_pk(root, info):
        return root.public_id

    class Meta:
        abstract = True
