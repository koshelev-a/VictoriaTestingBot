from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from app import database as db
from app import keyboards as kb
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('API_TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')


class NewQuestion(StatesGroup):
    section = State()
    creator = State()
    question = State()
    complexity = State()


# Первое сообщение 
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer(f'Это бот для прохождения еженедельного тестирования.', reply_markup = kb.main_menu)
    if message.from_user.id == int(os.getenv('ADMIN_ID')or('SUPERVISOR')):
        await message.answer(f'Вы являетесь администратором!', reply_markup = kb.main_menu_for_admin)

# Функция входа в админ-панель
@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')or('SUPERVISOR')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup = kb.admin_panel)
    else:
        await message.reply('Вы не администратор!')


# Создания вопроса в Админ-панели
@dp.message_handler(text='Добавить вопрос')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')or('SUPERVISOR')):
        await NewQuestion.section.set()
        await message.answer(f'Выберите тип вопроса', reply_markup = kb.catalog_list)
    else:
        await message.reply(f'Я тебя не понимаю.')

@dp.callback_query_handler(state = NewQuestion.section)
async def add_question_section(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['section'] = call.data
    await call.message.answer(f'Какой вопрос?', reply_markup = kb.cancel)
    addUserName= message.from_user.first_name
    await NewQuestion.next()

@dp.message_handler(state = NewQuestion.creator)
async def add_question_section(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['creator'] = from_user.first_name #Сделать что бы 
    await NewQuestion.next()

@dp.message_handler(state = NewQuestion.question)
async def add_question_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer(f'Какая сложность?', reply_markup = kb.cancel)
    await NewQuestion.next()

@dp.message_handler(state = NewQuestion.complexity)
async def add_question_complexity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['complexity'] = message.text
    await db.add_question(state)
    await message.answer(f'Вопрос успешно создан!', reply_markup = kb.admin_panel)
    await state.finish()


# Просмотр вопросов в Админ-панеле
@dp.message_handler(text = 'Посмотреть все вопросы')
async def cmd_check_all_questions(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')or('SUPERVISOR')):
        await message.answer(f'Для просмотра вопросов можно выбрать категорию или просмотреть абсолютно все вопросы которые есть в базе данных.', reply_markup = kb.check_all_qustions)
    else:
        await message.reply('Вы не администратор!')

# Вызов кнопкой "Все вопросы"
@dp.callback_query_handler(text = 'all_questions')
async def call_check_all_questions(call: types.CallbackQuery): 
        await call.message.answer(f'Загрузка...') # В ставить выгрузку с базы данных
        db.cur.execute('SELECT * FROM questions')
        all_questions = db.cur.fetchall()
        questions = ''
        for row in all_questions:
            questions += f"Вопрос №{row[0]}\nСоздал - {row[1]}\nВопрос: {row[2]}\nРаздел: {row[4]}\nСложность - {row[3]}\n\n"
        await call.message.answer(f'{questions}')

@dp.callback_query_handler(text = 'check_all_rooms')
async def call_check_all_rooms(call: types.CallbackQuery): 
        await call.message.answer(f'Загрузка...') # В ставить выгрузку с базы данных
        db.cur.execute('SELECT * FROM questions WHERE section = "all_rooms"')
        all_rooms = db.cur.fetchall()
        check_rooms_questions = ''
        for row in all_rooms:
            check_rooms_questions += f"Вопрос №{row[0]}\nСоздал - {row[1]}\nВопрос: {row[2]}\nРаздел: {row[4]}\nСложность - {row[3]}\n\n"
        await call.message.answer(f'{check_rooms_questions}')
        # if not check_rooms_questions():
        #     await call.message.answer(f'Вопросов по данному разделу ещё нет')


# from datetime import datetime /Нужно импортировать
# time_now = datetime.now().strftime('%H:%M') /Для получения данных о времени создания
# Если бот не понимает
@dp.message_handler()
async def answer(message: types.Message):
    await message.reply(f'Я тебя не понимаю')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)