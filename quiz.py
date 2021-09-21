import json
import random


def get_question_answers(number, data):
    question = data[number][str(number + 1)]["question"]
    answers = data[number][str(number + 1)]["answers"].split(', ')
    if len(answers) > 4:
        answers = data[number][str(number + 1)]["answers"].split('; ')
    return question, answers


def shuffle_answers(answers):
    random.shuffle(answers)
    return answers


def quiz_game(question, answers, correct_answer):
    print('Приветствую, пользователь! Сыграем в викторину!')
    print(question)
    for key, answer in zip((1, 2, 3, 4), answers):
        print(f"\t{key} - {answer}")
    user_answer = get_user_answer()
    if answers[user_answer - 1] == correct_answer:
        print(f'Вы великолепны! Правильный ответ действительно {correct_answer}')
    else:
        print(f'К сожалению, Вы ошиблись. правильный ответ - {correct_answer}')


def get_user_answer():
    while True:
        try:
            user_answer = int(input('Введите Ваш ответ:  '))
            if not 1 <= user_answer <= 4:
                raise ValueError
        except ValueError as exc:
            print('Выберите правильный ответ, введя число от 1 до 4!')
            continue
        else:
            break
    return user_answer


def main():
    with open("questions/questions.json", "r", encoding="utf-8") as inf:
        data = json.load(inf)
    number_question = random.randint(1, len(data))
    question, answers = get_question_answers(number_question, data)
    correct_answer = answers[0]
    answers = shuffle_answers(answers)
    quiz_game(question, answers, correct_answer)


if __name__ == '__main__':
    main()



