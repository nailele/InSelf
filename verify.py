from telebot import types
from config import bot
from markups import form_view_markup
from model import verify_form, not_verified, verified


def start_verify(message):
    bot.send_message(message.from_user.id, 'Ищем заявки...', reply_markup=types.ReplyKeyboardRemove())
    try:
        msg = bot.send_message(message.from_user.id, f'{verify_form()[0]}\n{verify_form()[1]}\n{verify_form()[2]}'
                                                     f'\n{verify_form()[3]}\n{verify_form()[4]}',
                               reply_markup=form_view_markup())
        bot.register_next_step_handler(msg, verify_choice)
    except Exception as e:
        print(e)
        msg = bot.send_message(message.from_user.id, 'Заявок на верификацию не найдено !',
                               reply_markup=form_view_markup())
        # bot.register_next_step_handler(msg, verify_choice)


def verify_choice(message):
    if message.text == '-':
        not_verified(verify_form()[5])
        msg = bot.send_message(message.from_user.id, 'Окей, идем дальше')
    elif message.text == '+':
        verified(verify_form()[5])
        msg = bot.send_message(message.from_user.id, 'Окей, идем дальше')
    bot.register_next_step_handler(msg, start_verify)
