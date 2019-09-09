import graphene

from minesweeper.service import Service
from .types import UserType


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)

    ok = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, _, password, first_name, last_name, email):
        try:
            service = Service()
            user = service.create_user(username=None,
                                       password=password,
                                       email=email)
            return CreateUser(ok=True, error=None, user=user)
        except Exception as e:
            return CreateUser(ok=False, error=str(e), user=None)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
