import random

from peewee import fn

import db


class Question:
    db_max_id = db.Question.select(fn.Max(db.Question.id)).scalar()

    def __init__(self):
        self.reinit_question()

    def reinit_question(self):
        random_id = random.randint(1, self.db_max_id + 1)

        question_db = (db.Question
                       .select()
                       .where(db.Question.id >= random_id)
                       .order_by(db.Question.id)
                       .limit(1)
                       .get()
                       )

        self.question_id = question_db.id
        self.question_body = question_db.body
        self.correct_answer = question_db.correct_answer
        self.answers = [
            question_db.correct_answer,
            question_db.other_answer_1,
            question_db.other_answer_2,
            question_db.other_answer_3,
        ]
        self.shuffle_answers()

    def shuffle_answers(self):
        random.shuffle(self.answers)

    def __str__(self):
        message = f"Вот твой вопрос:\n{self.question_body}\n"
        for index, answer in enumerate(self.answers, start=1):
            message += f"\t{index} - {answer}\n"
        return message
