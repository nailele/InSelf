import sqlalchemy
from telebot.types import ReplyKeyboardRemove
from config import bot
from model import add_name, add_age, add_about, add_number, add_gender
from markups import gender_markup



def name(message):
    add_name(message, message.from_user.id)
    msg = bot.send_message(message.from_user.id, 'Ваш пол', reply_markup=gender_markup())
    bot.register_next_step_handler(msg, gender)


def gender(message):
    # добавить обработку исключения когда вместо пола приходит херня
    add_gender(message, message.from_user.id)
    msg = bot.send_message(message.from_user.id, 'Возраст', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, age)


def age(message):
    # добавить обработку исключения когда приходит вместо цифр текст
    add_age(message, message.from_user.id)
    msg = bot.send_message(message.from_user.id, 'Расскажите о себе и о своем опыте')
    bot.register_next_step_handler(msg, about)


def about(message):
    # добавить обработку исключения когда приходит вместо цифр текст
    add_about(message, message.from_user.id)
    msg = bot.send_message(message.from_user.id, 'Введите ваш номер для связи')
    bot.register_next_step_handler(msg, number)


def number(message):
    add_number(message, message.from_user.id)
    msg = bot.send_message(message.from_user.id, 'Ваша заявка принята, ожидайте подтверждения')
    # bot.register_next_step_handler(msg, request_accepted)
