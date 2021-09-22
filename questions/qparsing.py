import requests
import json
from bs4 import BeautifulSoup


def generate_urls_from_baza_otvetov_ru():
    """
    The function generates a URL from the site baza-otvetov.ru
    first page with ten questions (1-10):https://baza-otvetov.ru/categories/view/1/
    second page with next ten questions(11-20): https://baza-otvetov.ru/categories/view/1/10...
    """
    main_url = "https://baza-otvetov.ru/categories/view/1/"
    pages = 0
    while pages <= 2000:
        if pages == 0:
            yield main_url
            pages += 10
        else:
            yield main_url + str(pages)
            pages += 10


def get_question_answers(soup):
    """
    The function receives as input the result of BeautifulSoup4 parsing HTML page with ten questions.
    Searches the HTML page for all rows(<tr>) in table with questions, and
    then breaks this rows into id, question and answers

    :param soup: BeatifulSoup format
    :return: list of dict with TEN questions
    """
    question_table_html = soup.find_all('tr', class_='tooltip')
    questions_dict = []
    for element in question_table_html:
        question_unformatted = element.text.strip().split('\n')
        try:
            id = str(question_unformatted[0])
            question = question_unformatted[2]
            answers = (question_unformatted[-1] + ',' + question_unformatted[-3].strip().split(':')[1])
        except IndexError:
            print(question_unformatted)
            continue
        questions_dict.append(write_questions_to_dict_format(id, question, answers))
    return questions_dict

def write_questions_to_dict_format(id, question, answers):
    """
    The function takes id, question and answers as input and creates a dict-record

    :param id: question's id in str format.
    :param question:  question in str format
    :param answers: answers in str format. Correct answer always in first place.
    :return: question in dict format
    """
    question_dict_format = {id: {"question": question, "answers": answers}}
    return question_dict_format


def write_questions_to_json_file(questions_list):
    """
    The function takes list of all questions in dict format as input and create a JSON-file.

    :param questions_list: question's list in dict format
    """
    with open("questions.json", 'w', encoding='utf-8') as ouf:
        json.dump(questions_list, ouf, ensure_ascii=False)

def main():
    """
    We parse each page, get out of every 10 questions in dict format and create a summary list with all the questions
    """
    question_list_json = []
    for url in generate_urls_from_baza_otvetov_ru():
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        question_list_json.extend(get_question_answers(soup))
    write_questions_to_json_file(question_list_json)


if __name__ == '__main__':
    main()