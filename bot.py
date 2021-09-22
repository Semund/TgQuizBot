import telebot
import question
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def quiz_game(message):
    if "вопрос" in message.text.lower():
        bot.send_message(
            message.chat.id,
            "Test question"
        )
    elif "игра" in message.text.lower():
        bot.send_message(
            message.chat.id,
            "Let's play!"
        )
    elif 'привет' in message.text.lower():
        bot.send_message(
            message.chat.id,
            f"Приветствую, {message.from_user.first_name}!\nПоиграем или просто вопрос?"
        )
    else:
        bot.reply_to(
            message,
            text=f"Я пока мало что умею, {message.from_user.first_name}. Поиграем или просто вопрос?"
        )


bot.polling()

# quiz.main()



# def get_user_answer():
#     """
#     Function waiting for input from the user until he enters the correct answer number in the range from 1 to 4
#     """
#     while True:
#         try:
#             user_answer = int(input('Введите Ваш ответ:  '))
#             if not 1 <= user_answer <= 4:
#                 raise ValueError
#         except ValueError as exc:
#             print('Выберите правильный ответ, введя число от 1 до 4!')
#             continue
#         else:
#             break
#     return user_answer