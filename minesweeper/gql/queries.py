import graphene

from minesweeper.gql.types import UserType, GameType
from minesweeper.service import Service


class DevigetQueries(graphene.ObjectType):
    users = graphene.List(UserType)
    game_list = graphene.Field(graphene.List(GameType), user_id=graphene.NonNull(graphene.Int))

    def resolve_users(self, info, **kwargs):
        service = Service()
        return service.users()

    def resolve_game_list(self, info, user_id, **kwargs):
        return Service().games(user_id)
