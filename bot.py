from telebot import types
import threading
import time
import telebot
from auth_bot import token
from scratch import scratch
from chatData import Chat_data
import string_const


def bot_init():
    data = {}
    brs_bot = telebot.TeleBot(token, parse_mode=None)


    def updates():
        while True:

            for chat_id in data.keys():
                print("обновлено у " + str(chat_id))
                time.sleep(20)
                curr_data = data[chat_id].user_data
                new_data = ''
                try:
                    new_data = scratch(data[chat_id].login, data[chat_id].password)
                except:
                    brs_bot.send_message(chat_id,
                                             "Проблемы с доступом к БРС")
                for i in range(1, len(curr_data)):
                    if int(curr_data[i].semester[0]) != data[chat_id].current_semester:
                        break
                    if curr_data[i].first_att[0] != new_data[i].first_att[0]:
                        data[chat_id].user_data = new_data
                        send_sticker(chat_id, int(new_data[i].first_att[0]))
                        brs_bot.send_message(chat_id,
                                             "Первая аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: " +
                                             new_data[i].first_att[0])
                    if curr_data[i].second_att[0] != new_data[i].second_att[0]:
                        data[chat_id].user_data = new_data
                        send_sticker(chat_id, int(new_data[i].second_att[0]))
                        brs_bot.send_message(chat_id,
                                             "Вторая аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: " +
                                             new_data[i].second_att[0])
                    if curr_data[i].third_att[0] != new_data[i].third_att[0]:
                        data[chat_id].user_data = new_data
                        send_sticker(chat_id, int(new_data[i].third_att[0]))
                        brs_bot.send_message(chat_id,
                                            "Третья аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: ")
                

            time.sleep(3600)

    thread = threading.Thread(target=updates)

    thread.start()

    @brs_bot.message_handler(commands=['start'])
    def send_welcome(message):
        data[message.chat.id] = Chat_data()
        brs_bot.send_message(message.chat.id, string_const.new_login)
        data[message.chat.id].login_exist_req = True

    @brs_bot.message_handler(content_types=['text'])
    def process_message(message):
        chat_id = message.chat.id
        message_text = message.text
        print()
        if chat_id not in data.keys():
            brs_bot.send_message(chat_id, string_const.error)
            return
        # data[chat_id].to_string()
        if data[chat_id].login_exist_req:
            if len(message_text.split(" ")) == 1:
                data[chat_id].login = message_text
                data[chat_id].login_exist_req = False
                brs_bot.send_message(chat_id, string_const.new_password)
                data[chat_id].password_exist_req = True
                return
            brs_bot.send_message(chat_id, string_const.login_isnt_valid)
        # data[chat_id].to_string()
        if data[chat_id].password_exist_req:
            if len(message_text.split(" ")) == 1:
                data[chat_id].password = message_text
                data[chat_id].password_exist_req = False
                brs_bot.send_message(chat_id, string_const.user_auth1)
                try:
                    data[chat_id].user_data = scratch(data[chat_id].login, data[chat_id].password)
                except:
                    data[message.chat.id].login_exist_req = True
                    brs_bot.send_message(chat_id, string_const.error)
                    brs_bot.send_message(message.chat.id, string_const.new_login)
                    return
                brs_bot.send_message(chat_id, string_const.user_auth2)
                data[chat_id].current_semester = int(data[chat_id].user_data[0].semester[0])
                data[chat_id].max_sem = data[chat_id].current_semester
                send_table(chat_id)
                return
            brs_bot.send_message(chat_id, string_const.password_isnt_valid)

    def message_generate(current_semester, data):
        text = 'Ваши результаты за ' + str(current_semester) + ' семестр: \n'
        for s in data:
            if s.semester[0] == str(current_semester):
                text = text + s.subject[0][0: 13] + "... : " + s.first_att[0] + " | " + s.second_att[0] + " | " + \
                       s.third_att[0] + ' --- ' + s.exam + '\n'
        return text

    def keyboard_generate(current_semester, max_semester):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if current_semester > 1:
            btn1 = types.InlineKeyboardButton(text='Предыдущий семестр', callback_data='preSem')
            keyboard.add(btn1)
        if current_semester != max_semester:
            btn3 = types.InlineKeyboardButton(text='Следующий семестр', callback_data='nextSem')
            keyboard.add(btn3)
        btn2 = types.InlineKeyboardButton(text='Обновить', callback_data='update')
        keyboard.add(btn2)
        return keyboard

    def send_table(chat_id):
        keyboard = keyboard_generate(current_semester=data[chat_id].current_semester,
                                     max_semester=data[chat_id].max_sem)
        text = message_generate(data[chat_id].current_semester, data[chat_id].user_data)
        brs_bot.send_message(chat_id, text, reply_markup=keyboard)

    @brs_bot.callback_query_handler(func=lambda callback: callback.data)
    def check_callback_data(callback):
        try:
            print(data)
            if callback.data == 'update':
                update(callback.message.chat.id)
                return

            if callback.data == 'nextSem':
                data[callback.message.chat.id].current_semester += 1
            if callback.data == 'preSem':
                data[callback.message.chat.id].current_semester -= 1
            text = message_generate(data[callback.message.chat.id].current_semester,
                                    data[callback.message.chat.id].user_data)
            kb = keyboard_generate(data[callback.message.chat.id].current_semester, data[callback.message.chat.id].max_sem)
            brs_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                      reply_markup=kb)
        except:
            pass

    def update(chat_id):
        curr_data = data[chat_id].user_data
        new_data = ''
        try:
            new_data = scratch(data[chat_id].login, data[chat_id].password)
        except:
            pass
        flag = True
        for i in range(1, len(curr_data)):
            if int(curr_data[i].semester[0]) != data[chat_id].current_semester:
                break
            if curr_data[i].first_att[0] != new_data[i].first_att[0]:
                flag = False
                send_sticker(chat_id, int(new_data[i].first_att[0]))
                brs_bot.send_message(chat_id, "Первая аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: " +
                                     new_data[i].first_att[0])
            if curr_data[i].second_att[0] != new_data[i].second_att[0]:
                flag = False
                send_sticker(chat_id, int(new_data[i].second_att[0]))
                brs_bot.send_message(chat_id, "Вторая аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: " +
                                     new_data[i].second_att[0])
            if curr_data[i].third_att[0] != new_data[i].third_att[0]:
                flag = False
                send_sticker(chat_id, int(new_data[i].third_att[0]))
                brs_bot.send_message(chat_id, "Третья аттестация. \nПредмет: " + new_data[i].subject[0] + " \nБалл: " +
                                     new_data[i].third_att[0])

        if flag:
            brs_bot.send_message(chat_id, "Изменений нет")
        data[chat_id].user_data = new_data
        send_table(chat_id)

    def send_sticker(chat_id, score):
        if (score < 25):
            brs_bot.send_sticker(chat_id,
                                 sticker="CAACAgIAAxkBAAEBmv9lORzCq9RqDJse4lKv8Oe5Zl7fVwAC_RUAAmKSWEi-UCy6ZfFEATAE")
            return
        if (score < 35):
            brs_bot.send_sticker(chat_id,
                                 sticker="CAACAgIAAxkBAAEBmwFlORzjPDmARO1fkPsYQHJYRiFAawACLxcAAooOSEhMJDWhNZESbDAE")
            return
        if (score < 45):
            brs_bot.send_sticker(chat_id,
                                 sticker="CAACAgIAAxkBAAEBmv1lORy6Rzhm0LtMP7oZ4U3UrG7bcgACwhUAAlAdSUhTlP1Qw1XqODAE")
            return
        if (score < 51):
            brs_bot.send_sticker(chat_id,
                                 sticker="CAACAgIAAxkBAAEBmvtlORyl3tTX9S6ZrK9-lK8H940ihwACZxoAAnfJYEircBqp9M_xRTAE")
            return
      while True:
    try:
      brs_bot.polling(none_stop=True)
    except:
      sleep(0.3)
