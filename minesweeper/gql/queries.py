import graphene

from minesweeper.gql.types import UserType


class DevigetQueries(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return None
