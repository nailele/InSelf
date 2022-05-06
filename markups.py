from telebot import types


def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user = types.KeyboardButton("Пользователь")
    psy = types.KeyboardButton("Психолог")
    markup = markup.add(user, psy)
    return markup


def gender_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m = types.KeyboardButton("Мужчина")
    w = types.KeyboardButton("Женщина")
    markup = markup.add(m, w)
    return markup


def start_verify_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton("Начнем!")
    markup = markup.add(yes)
    return markup


def form_view_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    no = types.KeyboardButton("-")
    yes = types.KeyboardButton("+")
    markup = markup.add(no, yes)
    return markup


def psy_work_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton("Начать")
    stop = types.KeyboardButton("Закончить")
    markup = markup.add(start, stop)
    return markup

def psy_work_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton("/Начать")
    markup = markup.add(start)
    return markup

def psy_work_stop_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop = types.KeyboardButton("/Закончить")
    markup = markup.add(stop)
    return markup


def ok_for_user_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ok = types.KeyboardButton('Я прочитал/ла инструкцию и готова к поиску своего консультанта')
    markup = markup.add(ok)
    return markup


def space_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    space = types.KeyboardButton('              ')
    markup = markup.add(space)
    return markup
