import json
import random


def get_question_and_answers(number, data):
    """
    The function receives as input a list of all questions in dict format and a random number.
    The question ID starts at 1, not 0, so we offset it
    Answers to some questions cannot be splitted by ', '.
    To do this, the separators have been changed to '; ' in JSON manually

    :param number: Random int value from 1 to the number of all question
    :param data: list of all questions in dict format
    :return: question in str format and answers in list format
    """
    question = data[number][str(number + 1)]["question"]
    answers = data[number][str(number + 1)]["answers"].split(', ')
    if len(answers) != 4:
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
    """
    Function waiting for input from the user until he enters the correct answer number in the range from 1 to 4
    """
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
    """
    We get a list of questions from a JSON file, choose a random number within the list indices.
    Remember the correct answer, it always in [0] index, then we shuffle the answers and send it to the user
    """
    with open("questions/questions.json", "r", encoding="utf-8") as inf:
        data = json.load(inf)
    number_question = random.randint(0, len(data) - 1)
    question, answers = get_question_and_answers(number_question, data)
    correct_answer = answers[0]
    answers = shuffle_answers(answers)
    quiz_game(question, answers, correct_answer)


if __name__ == '__main__':
    main()



