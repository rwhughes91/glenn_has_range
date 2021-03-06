from flask_graphql import GraphQLView

from .schema import schema
from .middleware import AuthorizationMiddleware

graphql_endpoint = GraphQLView.as_view(
    "graphql", graphiql=True, schema=schema, middleware=[AuthorizationMiddleware()]
)
