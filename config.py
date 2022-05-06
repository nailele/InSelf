import telebot

token = "5198139631:AAFI7PUPtEBUwZtMe29d9vFslUygdfWxS1c"

db = 'postgresql+psycopg2://postgres:nailele@localhost/postgres'

bot = telebot.TeleBot(token, threaded=False)
