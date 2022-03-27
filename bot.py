
from xml.etree.ElementTree import tostring
import telebot
from telebot import types
import time
import random
from config import token
import sqlite3
from messages import *

sqliteConnection = sqlite3.connect('db.db', check_same_thread=False)
cursor = sqliteConnection.cursor()
i = 0
bot = telebot.TeleBot(token)
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton(text = 'Начать')
    markup.add(start_button)
    bot.send_message(message.chat.id, m_hello, reply_markup = markup)
@bot.message_handler(func = lambda message: not message.from_user.is_bot)
def begin(message):
    isStopped = False
    if message.chat.type == 'private':
        if message.text == 'Начать':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            minus_button = types.KeyboardButton(text = "+")
            plus_button = types.KeyboardButton(text = "-")
            markup.add(minus_button,plus_button)
            bot.send_message(message.from_user.id, m_instruction,reply_markup=markup) 
        elif message.text == '-':
            global i
            spisok = cursor.execute("""SELECT name, gender FROM information_of_psych""")
            data = cursor.fetchall()
            try :  
                list_of_inf = []
                for value in data[i]:
                    list_of_inf.append(value)
                inf = ''
                for value in list_of_inf:
                    value = value + '\n'
                    inf += '' + value
                bot.send_message(message.from_user.id,inf) 
                i = i + 1
            except IndexError:
                i = 0
                bot.send_message(message.from_user.id,m_update) 
        elif message.text == '+':
            bot.send_message(message.from_user.id, m_sent)

                
bot.polling(none_stop=True, interval=0)