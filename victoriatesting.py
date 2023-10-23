import telebot
import sqlite3
from telebot import types # для указание типов
import random


API_TOKEN = '6198436491:AAFGv26aOxPsDeA_3Nxd1Yge_MdjGBRjB5M'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    # Создания таблицы
    connectSQL = sqlite3.connect('testing.sql')
    cur = connectSQL.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id int primary key, first_name varchar(50), last_name varchar(50), start_date, result int)')
    connectSQL.commit()

    # Внесение данных пользователя в базу данных
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    db_table_val(user_id = user_id, first_name = user_name, last_name = user_surname)

    # Сообщение с кнопкой для начала теста
    markup_inline = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton(text='Начать тест', callback_data='start_test')
    markup_inline.add(item)
    bot.send_message(message.chat.id, 'Что бы начать тест нажмите на кнопку', reply_markup=markup_inline) 

# Функция для добовления ФИО в Базу данных
def db_table_val(user_id: int, first_name: str, last_name: str):
    connectSQL = sqlite3.connect('testing.sql')
    cur = connectSQL.cursor()
    cur.execute('INSERT INTO users (user_id, first_name, last_name) VALUES (?, ?, ?)', (user_id, first_name, last_name)) # Надо сделать что бы появлялась дата начала теста
    connectSQL.commit()
    cur.close()
    connectSQL.close()

# CallBack
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'start_test':
        connectSQL = sqlite3.connect('testing.sql')
        cur = connectSQL.cursor()
        cur.execute(f'SELECT * FROM questions WHERE question')
        questions = cur.fetchall()
        print(questions)

        bot.send_message(call.message.chat.id, 'Тест начинается! Данные тестируемого внесены в базу данных.')
        bot.send_message(call.message.chat.id, 'Первый вопрос:')



# Команда для создания вопроса
@bot.message_handler(commands=['create_question'])
def create_question(message):

    # Создания таблицы c вопросами
    connectSQL = sqlite3.connect('testing.sql')
    cur = connectSQL.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS questions (user_id int primary_key, creator varchar(255), question varchar(255), answer varchar(255), date_added)')
    connectSQL.commit()
    cur.close()
    connectSQL.close()

    # Cообщения (создать)
    msg = bot.send_message(message.chat.id, 'Введите вопрос')
    bot.register_next_step_handler(msg, create_question_2)

# Подтверждения о создании вопроса
def create_question_2(message):
     create_question_db(message.from_user.id, message.from_user.first_name, message.text)
     bot.send_message(message.chat.id, 'Вопрос успешно загружин в базу данных!')
     # Сделать кнопки с добавлением ещё одного вопроса и просмотром всех вопросов

# Функция для создания вопроса
def create_question_db(user_id: int, creator: str, question: str):
        connectSQL = sqlite3.connect('testing.sql')
        cur = connectSQL.cursor()
        cur.execute('INSERT INTO questions (user_id, creator, question) VALUES (?, ?, ?)', (user_id, creator, question)) 
        connectSQL.commit()
        cur.close()
        connectSQL.close()


# Просмотр всех вопросов
@bot.message_handler(commands=['all_questions'])
def chech_all_questions(message):
    connectSQL = sqlite3.connect('testing.sql')
    cur = connectSQL.cursor()
    
    cur.execute(f'SELECT * FROM questions')
    questions = cur.fetchall()
    print(questions)
    
    info = ''
    for el in questions:
        info += f'Создатель: {el[1]}\nВопрос: {el[2]}\n\n'

    cur.close()
    connectSQL.close()

    bot.send_message(message.chat.id, info)



# @bot.message_handler(content_types=['text'])
# def problem(message):
#     bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!")
  

# @bot.message_handler(commands=['users'])
# def all_users(message):
#     connectSQL = sqlite3.connect('testing.sql')
#     cur = connectSQL.cursor()

#     cur.execute('SELECT * FROM users')
#     cur.fetchall()
#     cur.close()
#     connectSQL.close()



# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, "Напиши свое имя!")

# # Узнаем имя тестируемого человека
# @bot.message_handler(commands=['go'])
# def send_welcome(message):
#     bot.reply_to(message, "Напиши свое имя!")


bot.polling(none_stop=True)