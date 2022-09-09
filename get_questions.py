import json

import requests
from bs4 import BeautifulSoup

import db

def generate_urls_from_baza_otvetov_ru():
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


def format_question_data(question_unformatted_data):
    """
    question_unformatted_data example:
    ['1', '', 'В каком городе не работал великий композитор 18-го века Кристоф Виллибальд Глюк?',
    '', '\t\t\t\t\t\t\t\tОтветы для викторин: Милан, Вена, Париж\t\t\t\t\t\t\t', '', 'Берлин']

    question_data example:
    ['1', 'В каком городе не работал великий композитор 18-го века Кристоф Виллибальд Глюк?',
    'Ответы для викторин: Милан, Вена, Париж', 'Берлин']
    """
    question_data = [data.strip() for data in question_unformatted_data if data]

    answers = question_data[3] + ',' + question_data[2].removeprefix('Ответы для викторин:')
    if len(answers.split(', ')) != 4:
        raise ValueError

    question = (question_data[1], ) + tuple(answers.split(', '))
    return question


def get_question_answers(soup):
    """
    The function receives as input the result of BeautifulSoup4 parsing HTML page with ten questions.
    Searches the HTML page for all rows(<tr>) in table with questions, and
    then breaks this rows into id, question and answers

    :param soup: BeatifulSoup(html)
    :return: list
    """
    question_html_tr = soup.find_all('tr', class_='tooltip')
    questions_dict_list = []
    for element in question_html_tr:
        try:
            question = format_question_data(element.text.strip().split('\n'))
            questions_dict_list.append(question)
        except (ValueError, IndexError):
            continue

    return questions_dict_list


def write_questions_to_db(questions_list):
    """
    The function takes list of all questions in dict format as input and create a JSON-file.

    :param questions_list: question's list in dict format
    """
    with open("questions/questions.json", 'w', encoding='utf-8') as json_file:
        json.dump(questions_list, json_file, ensure_ascii=False)


def main():
    """
    We parse each page, get out of every 10 questions in dict format and create a summary list with all the questions
    """
    question_list = []
    for url in generate_urls_from_baza_otvetov_ru():
        html_document = requests.get(url).text
        soup = BeautifulSoup(html_document, 'html.parser')
        question_list.extend(get_question_answers(soup))
        break
    print(question_list)
    write_questions_to_json_file(question_list)


if __name__ == '__main__':
    main()
