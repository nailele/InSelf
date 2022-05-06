import sqlalchemy
from telebot.types import ReplyKeyboardRemove
import telebot
from config import bot
from model import session, Form, add_id, psy_work_active
from markups import start_verify_markup, start_markup, psy_work_start_markup, ok_for_user_markup, space_markup, \
    form_view_markup
from psy_dialog import name
from verify import start_verify


@bot.message_handler(commands=['start'])
def start(message):
    # if message.from_user.id == 2097693743:
    if message.from_user.id == 5171067586:
        msg = bot.send_message(message.from_user.id, 'Приветствую рабыня ! Ну что, начнем проверять завки !?',
                               reply_markup=start_verify_markup())
        bot.register_next_step_handler(msg, start_verify)

    else:
        msg = bot.send_message(message.from_user.id, 'Здравствуйте ! Вас приветствует бот.\nРасскажите нам, кто вы ?',
                               reply_markup=start_markup())
        bot.register_next_step_handler(msg, user_answer)


def user_answer(message):
    if message.chat.type == 'private':
        if message.text == 'Психолог':
            try:
                psy_exist = session.query(Form).filter(Form.psy_id == message.from_user.id).one()
                if psy_exist.psy_verify == 'No':
                    # добавить маркапы на переподачу заявки или редактирование
                    bot.send_message(message.from_user.id,
                                     'Ваша заявка на стадии проверки, желаете её отредактировать ?')
                # добавить маркапы на выход психолога в работу
                elif psy_exist.psy_verify == 'Yes':
                    msg = bot.send_message(message.from_user.id,
                                     'Вы уже состоите в нашей базе психологов, желаете начать работу ?',
                                     reply_markup=psy_work_start_markup())
                    bot.register_next_step_handler(msg, psy_work_active)
                # добавить маркапы на переподачу заявки
                if psy_exist.psy_verify == 'Viewed':
                    bot.send_message(message.from_user.id,
                                     'Ваша заявка была проверена и отклонена желаете переподать ?')
            except sqlalchemy.exc.NoResultFound:
                add_id(message)
                msg = bot.send_message(message.from_user.id, 'Начнем заполнение анкеты !\n Введите ваше ФИО',
                                       reply_markup=ReplyKeyboardRemove())
                bot.register_next_step_handler(msg, name)
        if message.text == 'Пользователь':
            msg = bot.send_message(message.from_user.id, 'Здесь должна быть инструкция для пользователя',
                                   reply_markup=ok_for_user_markup())

            bot.register_next_step_handler(msg, psy_search)


def active_psy():
    active_psy = session.query(Form).filter(Form.psy_status == 'Active').one()
    return active_psy

def approve(message):
    if message.text == '+':
        msg = bot.send_message(message.from_user.id, 'approve')
        # bot.register_next_step_handler(msg, psy_search)

    return

def decline(message):
    if message.text == '-':
        msg = bot.send_message(message.from_user.id, 'Идем дальше...')
        bot.register_next_step_handler(msg, psy_search)

def psy_search(message):
    try:

        msg = bot.send_message(message.from_user.id, 'Окей, мы подобрали вам психологов',
                               reply_markup=form_view_markup())
        # for psy in active_psy():
        msg = bot.send_message(message.from_user.id, f'{active_psy().psy_name}\n{active_psy().psy_age}\n'
                                                         f'{active_psy().psy_gender}\n{active_psy().psy_about}\n')
        bot.register_next_step_handler(msg, decline)
    except Exception as e:
        msg = bot.send_message(message.from_user.id, 'В данный момент нету работающих психологов')
        print(e)


if __name__ == "__main__":
    bot.infinity_polling('', skip_pending=True)
