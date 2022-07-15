import json
import random

with open("questions/questions.json", "r", encoding="utf-8") as inf:
    data = json.load(inf)


class Question:
    questions_list = data

    def __init__(self):
        self.reinit_question()

    def reinit_question(self):
        self.question = random.choice(self.questions_list)
        self.id_question = self.question['id']
        self.question_text = self.question['question']
        self.answers = self.question['answers'].split(', ')
        self.correct_answer = self.answers[0]
        self.shuffle_answers()

    def shuffle_answers(self):
        random.shuffle(self.answers)

    def __str__(self):
        message = f"Вот твой вопрос:\n{self.question_text}\n"
        for index, answer in enumerate(self.answers, start=1):
            message += f"\t{index} - {answer}\n"
        return message
