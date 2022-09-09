import os

import telebot
from telebot import types

import question as quest

TOKEN = os.getenv('TG_API_TOKEN')
bot = telebot.TeleBot(TOKEN)

MAIN_STATE = 'main'
QUIZ_STATE = 'quiz'

user_scores = {}
user_states = {}
user_questions = {}


def make_keyboard_to_chat():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False,
                                         input_field_placeholder='Нажми на кнопку!',
                                         resize_keyboard=True)

    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    btn5 = types.KeyboardButton('Вопрос')
    btn6 = types.KeyboardButton('Счет')
    keyboard.row(btn1, btn2, btn3, btn4)
    keyboard.row(btn5, btn6)
    return keyboard


@bot.message_handler(func=lambda message: True)
def dispatcher(user_tg_message):
    keyboard = make_keyboard_to_chat()

    user_id = user_tg_message.from_user.id
    user_name = user_tg_message.from_user.first_name
    if user_id not in user_scores.keys():
        user_scores[user_id] = {
            "wins": 0,
            "lose": 0
        }
    state = user_states.get(user_id, MAIN_STATE)

    if state == MAIN_STATE:
        main_handler(user_tg_message, user_id, user_name, keyboard)
    elif state == QUIZ_STATE:
        quiz_handler(user_tg_message, user_id, user_name, keyboard)


def main_handler(user_tg_message, user_id, user_name, keyboard):
    msg = ''

    if user_tg_message.text.lower() in ("да", "+", "вопрос"):
        get_new_question_and_send(keyboard, user_tg_message, user_id)
        user_states[user_id] = QUIZ_STATE
    elif "1счет" in user_tg_message.text.lower():
        msg = f"{user_name}, твой счет: победы - {user_scores[user_id]['wins']}\n" \
              f"поражения - {user_scores[user_id]['lose']}"
        bot.reply_to(user_tg_message, msg, reply_markup=keyboard)

    else:
        msg = f"Я не понимаю тебя, {user_name}"

    if msg:
        bot.reply_to(user_tg_message, msg, reply_markup=keyboard)


def check_answer_and_reply_to_user(user_tg_message, user_id, user_name, keyboard):
    user_answer = int(user_tg_message.text.strip())
    current_question = user_questions[user_id]

    if current_question.correct_answer == current_question.answers[user_answer - 1]:
        user_scores[user_id]["wins"] += 1
        msg = f"Совершенно верно, {user_name}! Еще вопрос?"
    else:
        user_scores[user_id]["lose"] += 1
        msg = f"Неправильный ответ, {user_name}!Правильный ответ - {current_question.correct_answer}\n" \
              f"Еще вопрос?"

    bot.reply_to(user_tg_message, msg, reply_markup=keyboard)
    user_states[user_id] = MAIN_STATE
    user_questions[user_id] = None


def quiz_handler(user_tg_message, user_id, user_name, keyboard):
    if user_tg_message.text.strip() in ("1", "2", "3", "4"):
        check_answer_and_reply_to_user(user_tg_message, user_id, user_name, keyboard)

    elif user_tg_message.text.lower() in ("вопрос",):
        get_new_question_and_send(keyboard, user_tg_message, user_id)

    elif "счет" in user_tg_message.text.lower():
        msg = f"2{user_name}, твой счет: победы - {user_scores[user_id]['wins']}, поражения " \
              f"{user_scores[user_id]['lose']}\n"
        bot.reply_to(user_tg_message, msg, reply_markup=keyboard)
    else:
        msg = f"Я не могу понять твой ответ, {user_name}\n" \
              f"Выбери ответ, введя число от 1 до 4"
        bot.reply_to(user_tg_message, msg, reply_markup=keyboard)


def get_new_question_and_send(keyboard, message, user_id):
    question = quest.Question()
    user_questions[user_id] = question
    bot.send_message(message.chat.id, str(question), reply_markup=keyboard)


try:
    bot.polling()
except telebot.ExceptionHandler as err:
    print(err)
