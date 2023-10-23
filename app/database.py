import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()


async def db_start():
    cur.execute('CREATE TABLE IF NOT EXISTS users ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'user_tg_id INTEGER,'
                'first_name VARCHAR(50),'
                'last_name VARCHAR(50))')

    cur.execute('CREATE TABLE IF NOT EXISTS questions ('
                'question_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'creator VARCHAR(50),'
                'question VARCHAR(255),'
                'complexity INTEGER,'
                'section VARCHAR(255))')
    db.commit()

# Запись пользователя в БД на старте (если его там ещё нет)
async def cmd_start_db(user_id):
    user = cur.execute('SELECT * FROM users WHERE user_tg_id == {key}'.format(key = user_id)).fetchone()
    if not user:
        cur.execute('INSERT INTO users (user_tg_id) VALUES ({key})'.format(key = user_id))
        db.commit()

# Добавления вопроса
async def add_question(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO questions (creator, question, complexity, section) VALUES (?, ?, ?, ?)",
                    (data['creator'], data['question'], data['complexity'], data['section']))
        db.commit()

# Ввывести все вопросы (Не работает)
async def cmd_check_all_questions():
    cur.execute('SELECT * FROM questions')
    all_questions = cur.fetchall()
    questions = ''
    for row in all_questions:
        questions += f"Вопрос №{row[0]}\nСоздал - {row[1]}\nВопрос: {row[2]}\nРаздел: {row[4]}\nСложность - {row[3]}"
        print(questions)