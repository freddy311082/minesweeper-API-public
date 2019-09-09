import graphene
import graphql_jwt

from minesweeper.gql.types import GameType
from minesweeper.service import Service
from .types import UserType


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)

    ok = graphene.Boolean(default_value=True)
    error = graphene.String(default_value=None)
    user = graphene.Field(UserType, default_value=None)

    @staticmethod
    def mutate(root, _, username, password,  email):
        try:
            service = Service()
            user = service.create_user(username=username,
                                       password=password,
                                       email=email)
            return CreateUser(user=user)
        except Exception as e:
            return CreateUser(ok=False, error=str(e))


class StartNewGame(graphene.Mutation):
    class Arguments:
        user_id = graphene.NonNull(graphene.Int)
        num_rows = graphene.NonNull(graphene.Int)
        num_cols = graphene.NonNull(graphene.Int)
        num_mines = graphene.NonNull(graphene.Int)

    ok = graphene.Boolean(default_value=True)
    error = graphene.String(default_value=None)
    game = graphene.Field(GameType, default_value=None)

    @staticmethod
    def mutate(root, _, user_id, num_rows, num_cols, num_mines):
        try:
            service = Service()
            game = service.create_new_game(user_id, num_rows, num_cols, num_mines)
            return StartNewGame(game=game)

        except Exception as e:
            return StartNewGame(ok=False, error=str(e))


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    start_new_game = StartNewGame.Field()
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
