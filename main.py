import time
import sqlalchemy
from telebot.types import ReplyKeyboardRemove
import telebot
from config import bot
from model import session, Form, add_id, psy_work_active
from markups import start_verify_markup, start_markup, psy_work_start_markup, ok_for_user_markup, form_view_markup, \
    psy_work_stop_markup
from psy_dialog import name
from verify import start_verify

count = 0


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == 2097693743:
    # if message.from_user.id == 5171067586:
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
                                     'Ваша заявка на стадии проверки, желаете её отредактировать/отменить ?')
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


def select_psy(message):
    global count
    if message.text == '+':
        try:
            msg = bot.send_message(message.from_user.id, 'Окей устанавливаем связь с психологом...')
            msg = bot.send_message(active_psy()[count].psy_id, 'Вас выбрали психологом !\n Что бы закончить работу '
                                                               'нажмите на кнопку.',
                                   reply_markup=psy_work_stop_markup())
            session.query(Form).filter(Form.psy_id == active_psy()[count].psy_id).\
                update({'psy_status': 'InWork', 'user_id': message.from_user.id})
            session.commit()
            time.sleep(1)


        except Exception as e:
            print(e, 'select_psy')
            active_psy()
            bot.send_message(message.from_user.id, 'Мы обновили наш список психологов\nПовторите ещё раз !')
    if message.text == '-':
        msg = bot.send_message(message.from_user.id, 'Идем дальше...')
        count = count + 1
        bot.register_next_step_handler(msg, psy_search)



def psy_search(message):
    global count
    try:

        msg = bot.send_message(message.from_user.id, 'Ищем психолога...',
                               reply_markup=form_view_markup())
        msg = bot.send_message(message.from_user.id, f'{active_psy()[count].psy_name}\n'
                                                     f'{active_psy()[count].psy_age}\n'
                                                     f'{active_psy()[count].psy_gender}\n'
                                                     f'{active_psy()[count].psy_about}\n')
        bot.register_next_step_handler(msg, select_psy)
    except Exception as e:
        count = 0
        msg = bot.send_message(message.from_user.id, 'Мы обновили наш список психологов\nПовторите ещё раз !')
        bot.register_next_step_handler(msg, psy_search)


def user_id_chatting(message):
    user_id = session.query(Form).filter(message.from_user.id == Form.user_id).first()
    user_id = user_id.user_id
    return user_id


def psy_id_chatting(message):
    psy_id = session.query(Form).filter(message.from_user.id == Form.user_id).first()
    psy_id = psy_id.psy_id
    return psy_id


def active_psy():
    active_psy = session.query(Form).filter(Form.psy_status == 'Active').all()
    return active_psy


@bot.message_handler(content_types=['text'])
def chatting(message):
    try:

        id = session.query(Form).filter(Form.user_id == message.from_user.id).first()
        if message.from_user.id == id.user_id:
            bot.copy_message(from_chat_id=message.from_user.id, chat_id=id.psy_id, message_id=message.id)

    except AttributeError:
        id = session.query(Form).filter(message.from_user.id == Form.psy_id).first()
        bot.copy_message(from_chat_id=message.from_user.id, chat_id=id.user_id, message_id=message.id)


if __name__ == "__main__":
    bot.infinity_polling('', skip_pending=True)
