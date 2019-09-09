import graphene

from minesweeper.gql.types import UserType
from minesweeper.service import Service


class DevigetQueries(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        service = Service()
        return service.users()
