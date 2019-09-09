from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

import django.utils.timezone


class Game(models.Model):
    started_at = models.DateTimeField(default=django.utils.timezone.now(), null=False)
    ended_at = models.DateTimeField(default=django.utils.timezone.now(), null=False)
    board = models.TextField(null=False)
    rows = models.IntegerField(null=False)
    cols = models.IntegerField(null=False)
    state = models.CharField(max_length=40, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)


class DBManager:

    def create_user(self, username, password, email):
        user = get_user_model().objects.create(username=username, password=password, email=email)
        if user:
            return user

        raise ValueError('Error creating the new user {}.'.format(username))

    def users(self):
        return User.objects.all()

    def user_games(self, user_id):
        games = Game.objects.filter(user_id__exact=user_id)
        return games

    def create_new_game(self, user_id, num_rows, num_cols, num_mines, board, state='NEW'):
        user = User.objects.get(pk=user_id)
        game = Game(board=board, rows=num_rows, cols=num_cols, state=state)
        game.user = user
        game.save()
        return game
