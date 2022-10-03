import os

from peewee import *

db = SqliteDatabase('quiz.db')


class Question(Model):
    body = TextField()
    correct_answer = CharField()
    other_answer_1 = CharField()
    other_answer_2 = CharField()
    other_answer_3 = CharField()

    class Meta:
        database = db


class Player(Model):
    telegram_id = CharField(unique=True)
    player_name = CharField(max_length=64, default='Незнакомец')
    player_state = CharField(default='rest')
    win = IntegerField(default=0)
    lose = IntegerField(default=0)

    class Meta:
        database = db


if not os.path.isfile('quiz.db'):
    db.connect()
    db.create_tables([Question, Player])
