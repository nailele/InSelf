from sqlalchemy.orm import sessionmaker
from config import db, bot
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Integer, Column, DateTime, Time, ForeignKey, String, Table, select, or_, and_, over, \
    update, Boolean, Date, Numeric, MetaData, create_engine

# from main import psy_work
from markups import psy_work_start_markup, psy_work_stop_markup

engine = create_engine(db)
conn = engine.connect()
metadata_obj = MetaData()
Base = declarative_base()
metadata_obj.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


class Form(Base):
    __tablename__ = "form"
    psy_id = Column(BigInteger, primary_key=True)
    psy_name = Column(String)
    psy_gender = Column(String)
    psy_age = Column(Integer)
    psy_about = Column(String)
    psy_number = Column(String)
    psy_verify = Column(String)
    user_id = Column(Integer)
    psy_status = Column(String)


def add_id(message):
    session.add(Form(
        psy_id=message.from_user.id,
        psy_verify='No'
    ))
    session.commit()


def add_name(message, chat_id):
    session.query(Form).filter(
        Form.psy_id == chat_id).update(
        {'psy_name': message.text}
    )
    session.commit()


def add_age(message, chat_id):
    session.query(Form).filter(
        Form.psy_id == chat_id).update(
        {'psy_age': message.text}
    )
    session.commit()


def add_gender(message, chat_id):
    session.query(Form).filter(
        Form.psy_id == chat_id).update(
        {'psy_gender': message.text}
    )
    session.commit()


def add_about(message, chat_id):
    session.query(Form).filter(
        Form.psy_id == chat_id).update(
        {'psy_about': message.text}
    )
    session.commit()


def add_number(message, chat_id):
    session.query(Form).filter(
        Form.psy_id == chat_id).update(
        {'psy_number': message.text}
    )
    session.commit()


def verify_form():
    form_list = []
    form_z = session.query(Form).filter(Form.psy_verify == 'No').first()
    form_list = [form_z.psy_name, form_z.psy_age, form_z.psy_gender, form_z.psy_about, form_z.psy_number, form_z.psy_id]
    return form_list


def verified(chat_id):
    try:
        msg = bot.send_message(verify_form()[5], 'Ваша заявка принята ! Желаете начать работу ?',
                               reply_markup=psy_work_start_markup())
        bot.register_next_step_handler(msg, psy_work_active)
    except Exception as e:
        print(f'Произошла ошибка при отправке сообщения авторизированному психологу\n{e}')
    session.query(Form).filter(Form.psy_id == chat_id).update({'psy_verify': 'Yes'})
    session.commit()


@bot.message_handler(commands=['Начать'])
def psy_work_active(message):
    session.query(Form).filter(Form.psy_id == message.from_user.id).update({'psy_status': 'Active'})
    session.commit()
    msg = bot.send_message(message.from_user.id, 'Ваша анкета активна! Ожидайте заявок',
                           reply_markup=psy_work_stop_markup())


@bot.message_handler(commands=['Закончить'])
def psy_work_paused(message):
    id = session.query(Form).filter(message.from_user.id == Form.psy_id).first()
    msg = bot.send_message(id.user_id,'Психолог остановил беседу')
    session.query(Form).filter(Form.psy_id == message.from_user.id).update({'psy_status': 'Paused', 'user_id': None})
    session.commit()
    msg = bot.send_message(message.from_user.id, 'Ваша анкета неактивна! Хорошего отдыха',
                           reply_markup=psy_work_start_markup())


def not_verified(chat_id):
    try:
        bot.send_message(verify_form()[5], 'Ваша заявка отклонена !')
    except Exception as e:
        print(f'Произошла ошибка при отправке сообщения не авторизированному психологу\n{e}')

    session.query(Form).filter(Form.psy_id == chat_id).update({'psy_verify': 'Viewed'})
    session.commit()