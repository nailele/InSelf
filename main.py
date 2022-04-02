import config
import telebot

from telebot import types
from database import Database
from messages import *


db = Database("db1.db")
bot = telebot.TeleBot(config.token, threaded=False)


@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton ("Начать")
    markup.add(item1)
    bot.send_message(message.chat.id, "Меню", reply_markup=markup)


@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        bot.send_message(chat_info[1], "❗Собеседник покинул чат")
        bot.send_message(message.chat.id, "❗Вы вышли из чата")
    else:
        bot.send_message(message.chat.id, '❗Вы не начали диалог')


@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton ("Начать")
    markup.add(item1)
    bot.send_message(message.chat.id, "Здравствуйте {0.first_name}! Вас приветствует InSelf бот.\nДля начала работы нажмите на 'Начать'".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        chat_two = db.get_chat()
        chat_info = db.get_active_chat(message.chat.id)
        if message.text == 'пр' or message.text == "хей":
            chat_two = db.get_chat()

            if message.text == 'созд':
                db.create_chat(message.chat.id, chat_two)
                bot.send_message(message.chat.id, 'чат создан')

                bot.send_message(chat_info[1], message.chat.id, message.message_id)
            else:
                mess = "✅Собеседник найден! Чтобы остановить диалог, нажми /stop"

                bot.send_message(message.chat.id, mess)
                bot.send_message(chat_two, mess)
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.chat.id, message.message_id)



        elif message.text == 'созд':
            db.create_chat(message.chat.id, chat_two)
            bot.send_message(message.chat.id, 'чат создан')

        elif message.text == 'псих':
            db.add_psyho(message.chat.id)
            bot.send_message(message.from_user.id, 'вы псих')

        elif message.text == '+':
            db.add_queue(message.chat.id)
            bot.send_message(message.from_user.id, 'Вы в очереди')

        elif message.text == '-чел':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, 'чел удален')

        elif message.text == '-псих':
            db.delete_psyho(message.chat.id)
            bot.send_message(message.chat.id, 'псих удален')

        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❗Вы не начали диалог')


@bot.message_handler(content_types=['voice', 'video_note', 'sticker', 'audio', 'dice', 'photo', 'video', 'animation'])
def hi(message):
    chat_info = db.get_active_chat(message.chat.id)
    bot.copy_message(chat_info[1], message.chat.id, message.message_id)


if __name__ == "__main__":
    bot.infinity_polling('', skip_pending=True)
















