from functools import wraps
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo


def context(f):
    """NOTE: Decorator to extract & inject context from GraphQL resolver arguments."""

    def gql_decorator(func):
        def wrapper(*args, **kwargs):
            info = next(
                (arg for arg in args if isinstance(arg, GraphQLResolveInfo)), None
            )
            return func(info.context, *args, **kwargs)

        return wrapper

    return gql_decorator


def logged_in_user_required(func):
    @wraps(func)
    @context(func)
    def wrapper(context, *args, **kwargs):
        if not context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action.")
        return func(context, *args, **kwargs)

    return wrapper
