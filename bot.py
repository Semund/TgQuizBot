import telebot
from telebot import types

import question as quest
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)

MAIN_STATE = 'main'
QUIZ_STATE = 'quiz'

user_scores = {}
user_states = {}
user_questions = {}


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
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

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if message.from_user.id not in user_scores.keys():
        user_scores[message.from_user.id] = {
            "wins": 0,
            "lose": 0
        }
    state = user_states.get(user_id, MAIN_STATE)

    if state == MAIN_STATE:
        main_handler(message, user_id, user_name, keyboard)
    elif state == QUIZ_STATE:
        quiz_handler(message, user_id, user_name, keyboard)


def main_handler(message, user_id, user_name, keyboard):
    if message.text.lower() in ("да", "+", "вопрос"):
        get_new_question_and_send(keyboard, message, user_id)
        user_states[user_id] = QUIZ_STATE
    elif "счет" in message.text.lower():
        msg = f"{user_name}, твой счет: победы - {user_scores[user_id]['wins']}, поражения " \
              f"{user_scores[user_id]['lose']}\n"
        bot.reply_to(message, msg, reply_markup=keyboard)

    else:
        bot.reply_to(message, text=f"Я не понимаю тебя, {user_name}\n", reply_markup=keyboard)


def quiz_handler(message, user_id, user_name, keyboard):
    if message.text.strip() in ("1", "2", "3", "4"):
        user_answer = int(message.text.strip())
        current_question = user_questions[user_id]

        if current_question.correct_answer == current_question.answers[user_answer - 1]:
            user_scores[user_id]["wins"] += 1
            msg = f"Совершенно верно, {user_name}!\n" \
                  f"Еще вопрос?"
        else:
            user_scores[user_id]["lose"] += 1
            msg = f"Неправильный ответ, {user_name}!\n"
            msg += f"Правильный ответ - {current_question.correct_answer}\n" \
                   f"Твой счет: победы - {user_scores[user_id]['wins']}, поражения " \
                   f"{user_scores[user_id]['lose']}\n" \
                   f"Еще вопрос?"

        bot.send_message(message.chat.id, msg, reply_markup=keyboard)
        user_states[user_id] = MAIN_STATE
        user_questions[user_id] = None

    elif message.text.lower() in ("вопрос",):
        get_new_question_and_send(keyboard, message, user_id)

    elif "счет" in message.text.lower():
        msg = f"{user_name}, твой счет: победы - {user_scores[user_id]['wins']}, поражения " \
              f"{user_scores[user_id]['lose']}\n"
        bot.reply_to(message, msg, reply_markup=keyboard)
    else:
        bot.reply_to(
            message,
            text=f"Я не могу понять твой ответ, {user_name}\n"
                 f"Выбери ответ, введя число от 1 до 4",
            reply_markup=keyboard
        )


def get_new_question_and_send(keyboard, message, user_id):
    question = quest.Question()
    user_questions[user_id] = question
    bot.send_message(message.chat.id, str(question), reply_markup=keyboard)


bot.polling()
