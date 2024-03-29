""" File for router definition. Query and Mutation schemas for GraphQLRouter are setup."""
import strawberry
from strawberry.fastapi import GraphQLRouter

from api.schema import history_query_schema, url_shorten_mutation_schema
from context import get_url_context


@strawberry.type
class Query(history_query_schema.Query):
    """Query of service

    """
    ...


@strawberry.type
class Mutation(url_shorten_mutation_schema.Mutation):
    """Mutation of main service. Multiple mutations are allowed.

    Args:
        book_mutation_schema (Mutation): Book mutation schema
    """
    ...


schema = strawberry.Schema(query=Query, mutation=Mutation)
url_shortener_app = GraphQLRouter(schema, context_getter=get_url_context)
