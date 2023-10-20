import telebot
from auth_bot import token
from scratch import scratch

def bot_init():
    brs_bot = telebot.TeleBot(token, parse_mode=None)

    @brs_bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        brs_bot.reply_to(message, "Howdy, how are you doing?")

    @brs_bot.message_handler(commands=['join'])
    def send_join(message):
        print(message)
        brs_bot.reply_to(message, "чзх")

    @brs_bot.message_handler(content_types=['text'])
    def process_message(message):
        # Получить данные от пользователя
        text = message.text.split(" ")
        data = scratch(text[0], text[1])
        for dt in data:
            brs_bot.send_message(message.chat.id, dt)






    brs_bot.polling()



