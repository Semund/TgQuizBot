import requests
from bs4 import BeautifulSoup

import db


def generate_urls_from_source_paging():
    """
    The function generates a URL from the site baza-otvetov.ru
    first page with ten questions (1-10):https://baza-otvetov.ru/categories/view/1/
    second page with next ten questions(11-20): https://baza-otvetov.ru/categories/view/1/10...
    """
    main_url = "https://baza-otvetov.ru/categories/view/1/"
    questions = 0
    while questions <= 2550:
        if questions == 0:
            yield main_url
            questions += 10
        else:
            yield main_url + str(questions)
            questions += 10


def get_questions_list(soup):
    """
    The function receives as input the result of BeautifulSoup4 parsing HTML page with ten questions.
    Searches the HTML page for all rows(<tr>) in table with questions, and
    then breaks this rows into id, question and answers

    :param soup: BeatifulSoup(html)
    :return: list
    """
    questions_html = soup.find_all('tr', class_='tooltip')
    questions_list = []
    for element in questions_html:
        try:
            question = get_question(element.text.strip().split('\n'))
            questions_list.append(question)
        except (ValueError, IndexError):
            continue

    return questions_list


def get_question(question_unformatted_data):
    """
    question_unformatted_data example:
    ['1', '', 'В каком городе не работал великий композитор 18-го века Кристоф Виллибальд Глюк?',
    '', '\t\t\t\t\t\t\t\tОтветы для викторин: Милан, Вена, Париж\t\t\t\t\t\t\t', '', 'Берлин']

    question_data example:
    ['1', 'В каком городе не работал великий композитор 18-го века Кристоф Виллибальд Глюк?',
    'Ответы для викторин: Милан, Вена, Париж', 'Берлин']
    """
    question_data = [data.strip() for data in question_unformatted_data if data]

    question_body = question_data[1]
    question_correct_answer = question_data[-1]

    other_answers = question_data[2].removeprefix('Ответы для викторин: ').split(', ')
    if len(other_answers) != 3:
        raise ValueError

    question = {
        'body': question_body,
        'correct_answer': question_correct_answer,
        'other_answer_1': other_answers[0],
        'other_answer_2': other_answers[1],
        'other_answer_3': other_answers[2],
    }
    return question


def write_questions_to_db(questions_list):
    db.Question.insert_many(questions_list).execute()


def main():
    """
    We parse each page, get out of every 10 questions in dict format and write to db
    """

    for url in generate_urls_from_source_paging():
        try:
            response = requests.get(url)
        except requests.RequestException:
            continue

        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            question_list = get_questions_list(soup)
            write_questions_to_db(question_list)


if __name__ == '__main__':
    main()
