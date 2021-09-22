import json
import random

with open("questions/questions.json", "r", encoding="utf-8") as inf:
    data = json.load(inf)


class Question:
    questions_list = data

    def __init__(self):
        self.reinit_question()

    def reinit_question(self):
        self.question_dict = random.choice(Question.questions_list)
        self.id_question = self.get_id_question()
        self.question = self.get_question()
        self.answers = self.get_answers()
        self.correct_answer = self.answers[0]
        self.shuffle_answers()

    def get_id_question(self):
        for id in self.question_dict.keys():
            id_question = id
            if id_question:
                return id_question

    def get_question(self):
        question = self.question_dict[self.id_question]["question"]
        return question

    def get_answers(self):
        answers = self.question_dict[self.id_question]["answers"].split(', ')
        if len(answers) != 4:
            answers = self.question_dict[self.id_question]["answers"].split('; ')
        return answers

    def shuffle_answers(self):
        random.shuffle(self.answers)

    def __str__(self):
        message = f"Вот твой вопрос:\n{self.question}\n"
        for index, answer in enumerate(self.answers, start=1):
            message += f"\t{index} - {answer}\n"
        return message
