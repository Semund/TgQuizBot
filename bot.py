import telebot
import question as quest
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)
question = quest.Question()
flag_question = None

@bot.message_handler(func=lambda message: True)
def quiz_game(message):
    global flag_question
    if message.text.lower() in("да", "+", "вопрос"):
        question.reinit_question()
        bot.send_message(
            message.chat.id,
            str(question)
        )
        flag_question= True
    elif message.text.strip() in ("1", "2", "3", "4"):
        if flag_question:
            user_answer = int(message.text.strip())
            if question.correct_answer == question.answers[user_answer - 1]:
                msg = f"Совершенно верно, {message.from_user.first_name}! " \
                          f"Правильный ответ - {question.correct_answer}\nЕще один?"
            else:
                msg = f"Неправильный ответ, {message.from_user.first_name}! " \
                          f"Правильный ответ - {question.correct_answer}\nЕще один?"
            bot.send_message(
                message.chat.id,
                msg
            )
            flag_question = None
        else:
            bot.reply_to(
                message,
                text=f"Я не задавал тебе вопрос, {message.from_user.first_name}\n"
                     f"Я могу задать его тебе, просто напиши мне \"вопрос\""
            )
    elif 'привет' in message.text.lower():
        bot.send_message(
            message.chat.id,
            f"Приветствую, {message.from_user.first_name}!\nЯ могу задать тебе вопрос, просто напиши мне \"вопрос\""
        )
    else:
        bot.reply_to(
            message,
            text=f"Я пока не понимаю тебя, {message.from_user.first_name}\n"
                 f"Я могу только задать тебе вопрос, если ты напишешь мне \"вопрос\""
        )


bot.polling()
