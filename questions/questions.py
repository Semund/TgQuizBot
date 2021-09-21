import requests
import json
from bs4 import BeautifulSoup


def generate_urls_from_baza_otvetov_ru():
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
    question_table = soup.find_all('tr', class_='tooltip')
    questions_json = []
    for element in question_table:
        question_list = element.text.strip().split('\n')
        try:
            id = str(question_list[0])
            question = question_list[2]
            answers = (question_list[-1] + ',' + question_list[-3].strip().split(':')[1])
        except:
            print(question_list)
            continue
        questions_json.append(write_questions_to_json_format(id, question, answers))
    return questions_json

def write_questions_to_json_format(id, question, answers):
    question_json = {id: {"question": question, "answers": answers}}
    return question_json


def write_questions_to_json_file(questions_list):
    with open("questions.json", 'w', encoding='utf-8') as ouf:
        json.dump(questions_list, ouf, ensure_ascii=False)

def main():
    question_list_json = []
    for url in generate_urls_from_baza_otvetov_ru():
        print(url)
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        question_list_json.extend(get_question_answers(soup))
    write_questions_to_json_file(question_list_json)


if __name__ == '__main__':
    main()