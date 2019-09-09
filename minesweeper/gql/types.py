import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from minesweeper.models import Game


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

