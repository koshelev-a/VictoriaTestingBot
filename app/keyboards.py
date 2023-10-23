from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('Пройти тест').add('Подготовится к тесту')

main_menu_for_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_for_admin.add('Пройти тест').add('Подготовится к тесту').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить вопрос').add('Редактировать вопрос').add('Посмотреть все вопросы').add('Удалить вопрос')

# Метод для кнопок под текстом отправленый ботом
# catalog_list = InlineKeyboardMarkup()
# catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='ууу'),
#                  InlineKeyboardButton(text='', url=''),
#                  InlineKeyboardButton(text='', callback_data='dd'))

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Номерной фонд', callback_data='all_rooms'),
                 InlineKeyboardButton(text='Информация об отели', callback_data='hotel_information'),
                 InlineKeyboardButton(text='Кассовая десциплина', callback_data='cash_discipline'),
                 InlineKeyboardButton(text='Вопросы гостей', callback_data='questions_from_guests'),
                 InlineKeyboardButton(text='Конфликтные ситуации', callback_data='conflict_situations'),
                 InlineKeyboardButton(text='OPERA PMS', callback_data='opera_pms'))

check_all_qustions = InlineKeyboardMarkup(row_width=2)
check_all_qustions.add(InlineKeyboardButton(text = 'Все вопросы', callback_data = 'all_questions'),
                       InlineKeyboardButton(text = 'Номерной фонд', callback_data = 'check_all_rooms'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')