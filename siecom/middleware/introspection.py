from graphql.type import GraphQLField, GraphQLObjectType, GraphQLSchema, GraphQLString


class GrapheneBlockIntrospectionMiddleware:
    def resolve(self, next, root, info, **kwargs):
        if info.field_name.lower() in ["__schema", "_introspection"]:
            query = GraphQLObjectType(
                "Query",
                lambda: {
                    "Hello": GraphQLField(GraphQLString, resolve=lambda *_: "World")
                },
            )
            info.schema = GraphQLSchema(query=query)
            return next(root, info, **kwargs)
        return next(root, info, **kwargs)
