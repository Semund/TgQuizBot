import os

import telebot
from telebot import types

import db
import question as q

TOKEN = os.getenv('TG_API_TOKEN')
bot = telebot.TeleBot(TOKEN)

MAIN_STATE = 'rest'
QUIZ_STATE = 'quiz'
questions_cache = {}


@bot.message_handler(func=lambda message: True)
def dispatcher(player_telegram_session):
    keyboard = make_keyboard_to_chat()

    player_db = get_player_data_from_db(player_telegram_session)
    if player_db.player_state == MAIN_STATE:
        main_handler(player_db, player_telegram_session, keyboard)
    elif player_db.player_state == QUIZ_STATE:
        quiz_handler(player_db, player_telegram_session, keyboard)


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


def get_player_data_from_db(player_telegram_session):
    player_telegram_id = player_telegram_session.from_user.id
    player_db, _ = db.Player.get_or_create(telegram_id=player_telegram_id)
    player_db.player_name = player_telegram_session.from_user.first_name
    if questions_cache.get(player_db.telegram_id, None) is None:
        player_db.player_state = MAIN_STATE
    player_db.save()
    return player_db


def main_handler(player_db, player_telegram_session, keyboard):
    msg = ''

    if player_telegram_session.text.lower() in ("да", "+", "вопрос"):
        get_new_question_and_send(player_db, player_telegram_session, keyboard)
        player_db.player_state = QUIZ_STATE
        player_db.save()
    elif "счет" in player_telegram_session.text.lower():
        msg = f"{player_db.player_name}, твой счет: победы - {player_db.win}\n" \
              f"поражения - {player_db.lose}"
    else:
        msg = f"Я не понимаю тебя, {player_db.player_name}"

    if msg:
        bot.reply_to(player_telegram_session, msg, reply_markup=keyboard)


def quiz_handler(player_db, player_telegram_session, keyboard):
    msg = ''
    if player_telegram_session.text.strip() in ("1", "2", "3", "4"):
        check_answer_and_reply_to_player(player_db, player_telegram_session, keyboard)

    elif player_telegram_session.text.lower() in ("вопрос",):
        get_new_question_and_send(player_db, player_telegram_session, keyboard)
        player_db.lose += 1
        player_db.save()

    elif "счет" in player_telegram_session.text.lower():
        msg = f"{player_db.player_name}, твой счет: победы - {player_db.win}, поражения " \
              f"{player_db.lose}\n"
    else:
        msg = f"Я не могу понять твой ответ, {player_db.player_name}\n" \
              f"Выбери ответ, введя число от 1 до 4"

    if msg:
        bot.reply_to(player_telegram_session, msg, reply_markup=keyboard)


def get_new_question_and_send(player_db, player_telegram_session, keyboard):
    question = q.Question()
    questions_cache[player_db.telegram_id] = question
    bot.send_message(player_telegram_session.chat.id, str(question), reply_markup=keyboard)


def check_answer_and_reply_to_player(player_db, player_telegram_session, keyboard):
    player_answer = int(player_telegram_session.text.strip())
    current_question = questions_cache[player_db.telegram_id]

    if current_question.correct_answer == current_question.answers[player_answer - 1]:
        player_db.win += 1
        msg = f"Совершенно верно, {player_db.player_name}! Еще вопрос?"
    else:
        player_db.lose += 1
        msg = f"Неправильный ответ, {player_db.player_name}! Правильный ответ - {current_question.correct_answer}\n" \
              f"Еще вопрос?"

    bot.reply_to(player_telegram_session, msg, reply_markup=keyboard)
    player_db.player_state = MAIN_STATE
    player_db.save()
    questions_cache.pop(player_db.telegram_id)


try:
    bot.polling()
except telebot.ExceptionHandler as err:
    print(err)
