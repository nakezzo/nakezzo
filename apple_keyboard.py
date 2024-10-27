import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3


#Меню
def menu_keyboard(us_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT admin FROM apple WHERE user_id = ('%s')"%(us_id))
    admin = cursor.fetchone()[0]
    try:
        if admin == 1:
            menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
            menu_keyboard.add('🎮 Игры', '🙎🏼‍♂️ Профиль')
            menu_keyboard.add('⭐️ Избранные игры')
            menu_keyboard.add('ℹ️ Информация')
            menu_keyboard.add('Админка')
            return menu_keyboard
        if admin != 1:
            menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,  row_width=2)
            menu_keyboard.add('🎮 Игры', '🙎🏼‍♂️ Профиль')
            menu_keyboard.add('⭐️ Избранные игры')
            menu_keyboard.add('ℹ️ Информация')
            return menu_keyboard
    except:
            menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,  row_width=2)
            menu_keyboard.add('🎮 Игры', '🙎🏼‍♂️ Профиль')
            menu_keyboard.add('⭐️ Избранные игры')
            menu_keyboard.add('ℹ️ Информация')
            return menu_keyboard
    return menu_keyboard

def vivod_keyboard():
    vivod_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    vivod_keyboard.add('QIWI')
    return vivod_keyboard

#Выбор типа игр
game_type_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text = '🕹 Одиночная', callback_data = 'solo_games')
btn2 = types.InlineKeyboardButton(text = '🖲 С игроками', callback_data = 'pvp_games')
game_type_keyboard.add(btn1, btn2)


#Одиночные Игры
game_keyboard = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton(text='🍏 Apple', callback_data='apple')
#btn2 = types.InlineKeyboardButton(text='🕹 Triple', callback_data='triple')
#btn3  = types.InlineKeyboardButton(text = '💣 Mines', callback_data = 'mines')
btn4 = types.InlineKeyboardButton(text = '◀️ Назад', callback_data = 'rejimi')
game_keyboard.add(btn1)
game_keyboard.add(btn4)

#pvp игры 
pvp_game_keyboard = types.InlineKeyboardMarkup(row_width = 2)
btn1 = types.InlineKeyboardButton(text = '🎲 Кубик', callback_data = 'cube')
btn2 = types.InlineKeyboardButton(text = '🎳 Боулинг', callback_data = 'bouling')
btn3 = types.InlineKeyboardButton(text = '🏀 Баскетбол', callback_data = 'backetball')
btn4 = types.InlineKeyboardButton(text = '🎯 Дартс', callback_data = 'dartc')
btn5 = types.InlineKeyboardButton(text = '⚽ Футбол', callback_data = 'football')
btn6 = types.InlineKeyboardButton(text = '🎰 Автомат', callback_data = 'avtomat')
btn7 = types.InlineKeyboardButton(text = '◀️ Назад', callback_data = 'rejimi')
#btn8 = types.InlineKeyboardButton(text = '♥️♠️ BlackJack', callback_data = 'BlackJack')
pvp_game_keyboard.add (btn1, btn2, btn3, btn5, btn4, btn6)
pvp_game_keyboard.add (btn7)

pvp_spisok_keyboard = types.InlineKeyboardMarkup(row_width = 2)
btn1 = types.InlineKeyboardButton(text = '🎲 Кубик', callback_data = 'cube')
btn2 = types.InlineKeyboardButton(text = '🎳 Боулинг', callback_data = 'bouling')
btn3 = types.InlineKeyboardButton(text = '🏀 Баскетбол', callback_data = 'backetball')
btn4 = types.InlineKeyboardButton(text = '🎯 Дартс', callback_data = 'dartc')
btn5 = types.InlineKeyboardButton(text = '⚽ Футбол', callback_data = 'football')
btn6 = types.InlineKeyboardButton(text = '🎰 Автомат', callback_data = 'avtomat')
btn7 = types.InlineKeyboardButton(text = '◀️ Назад', callback_data = 'favorite_list')
#btn8 = types.InlineKeyboardButton(text = '♥️♠️ BlackJack', callback_data = 'BlackJack')
pvp_spisok_keyboard.add (btn1, btn2, btn3, btn5, btn4, btn6)
pvp_spisok_keyboard.add (btn7)


#карта mines
mines_keyboard = types.InlineKeyboardMarkup(row_width = 5)
mines_map = {'mines_A1': '🔘','mines_A2': '🔘','mines_A3': '🔘','mines_A4': '🔘','mines_A5': '🔘',
            'mines_B1': '🔘','mines_B2': '🔘','mines_B3': '🔘','mines_B4': '🔘','mines_B5': '🔘',
            'mines_C1': '🔘','mines_C2': '🔘','mines_C3': '🔘','mines_C4': '🔘','mines_C5': '🔘',
            'mines_D1': '🔘','mines_D2': '🔘','mines_D3': '🔘','mines_D4': '🔘','mines_D5': '🔘',
            'mines_E1': '🔘','mines_E2': '🔘','mines_E3': '🔘','mines_E4': '🔘','mines_E5': '🔘'}
button_list = [types.InlineKeyboardButton(text = v, callback_data = key) for key, v in mines_map.items()]
close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='close_game')
mines_keyboard.add(*button_list, close_game)

#Карта яблок
apple_keyboard_start = types.InlineKeyboardMarkup(row_width=5)
apples_map = { 'key6_A1': '🔘', 'key6_A2': '🔘', 'key6_A3': '🔘', 'key6_A4': '🔘', 'key6_A5': '🔘',
                  'key5_B1': '🔘', 'key5_B2': '🔘', 'key5_B3': '🔘', 'key5_B4': '🔘', 'key5_B5': '🔘',
                  'key4_C1': '🔘', 'key4_C2': '🔘', 'key4_C3': '🔘', 'key4_C4': '🔘', 'key4_C5': '🔘',
                  'key3_D1': '🔘', 'key3_D2': '🔘', 'key3_D3': '🔘', 'key3_D4': '🔘', 'key3_D5': '🔘',
                  'key2_E1': '🔘', 'key2_E2': '🔘', 'key2_E3': '🔘', 'key2_E4': '🔘', 'key2_E5': '🔘',
                  'key1_F1': '🔘', 'key1_F2': '🔘', 'key1_F3': '🔘', 'key1_F4': '🔘', 'key1_F5': '🔘'}
button_list = [types.InlineKeyboardButton(text=v, callback_data=key) for key, v in apples_map.items()]
close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='close_game')
apple_keyboard_start.add(*button_list, close_game)

#Карта Triple
triple_keyboard = types.InlineKeyboardMarkup(row_width=3)
triple_map = {'dice_A1': ' ', 'dice_A2': ' ', 'dice_A3': ' ', 
              'dice_B1': ' ', 'dice_B2': 'start', 'dice_B3': ' ',
              'dice_C1': ' ', 'dice_C2': ' ', 'dice_C3': ' '}
triple_keyboard = types.InlineKeyboardMarkup(row_width=3)
button_list = [types.InlineKeyboardButton(text=v, callback_data=key) for key, v in triple_map.items()]
close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='close_game')
triple_keyboard.add(*button_list, close_game)

#Админменю
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
admin_keyboard.add('Меню подкрутки')
admin_keyboard.add('Снять прибыль с PVP игр','Снять кассу','Создать промокод', 'Обнулить игру', 'Изменить мин. ставку','Изменить макс. ставку', 'Изменить антиминус','Подключить к партнерке','Настройка CristalPAY', 'Изменить QIWI KEY','Подключить к партнерке','Отключить от партнерки', 'Сделать рассылку', 'Выдать/Забрать баланс', 'Выдать админку', 'В меню')

#Да\нет
nazad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
nazad.add('Админка')

#Настройка кассы
setting_kassa = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
setting_kassa.add('Снять кассу', 'Изменить антиминус', 'Админка')

#Отмена
otmena_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
otmena_keyboard.add('Отмена')

#Отмена
otmena_inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text='Отменить', callback_data='otmena')
otmena_inline_keyboard.add(btn1)

#Пополнение
payments_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text='Qiwi', callback_data='Qiwi')
payments_keyboard.add(btn1)

#Проверка киви

deposit_btn = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text="🔁Проверить оплату", callback_data='check_payment')
button2 = types.InlineKeyboardButton(text="❌Отменить  оплату", callback_data="undo_payment")
deposit_btn.row(button1)
deposit_btn.add(button2)

#Соглашение
sogl_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text="✅ Принять правила", callback_data="ya_soglasen")
sogl_keyboard.row(btn1)

#Подтверждение вывода
def confirm_keyboard(us_id):
    confirm_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="✅ Выплатить", callback_data=f"viplatit{us_id}")
    btn2 = types.InlineKeyboardButton(text="❌ Отклонить", callback_data=f"otklonit{us_id}")
    confirm_keyboard.add(btn1, btn2)
    return confirm_keyboard

#Отклонено
otkloneno_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text="❌ Отклонено", callback_data=f"otklon")
otkloneno_keyboard.add(btn1)

#Выплачено
viplacheno_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text="✅ Выплачено", callback_data=f"otklon")
viplacheno_keyboard.add(btn1)

#Закрытие уведомлений
close_message_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(text="❌ Закрыть", callback_data='close_message')
close_message_keyboard.add(btn1)

#Спрятать клавиатуру
hideBoard = types.ReplyKeyboardRemove()

vibor_plata_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width = 2)
vibor_plata_keyboard.add('QIWI','CristalPAY')
vibor_plata_keyboard.add('В меню')

#Профиль
profile_keyboard = types.InlineKeyboardMarkup(row_width=2)
btn1 = InlineKeyboardButton(text="💸 Активировать промокод", callback_data='start_promo')
btn2 = InlineKeyboardButton(text="📥 Пополнить", callback_data='popolnenie')
btn3 = InlineKeyboardButton(text="📥 Вывод", callback_data='vivodbabla')
btn4 = InlineKeyboardButton(text="🎁 Реферальная программа", callback_data = 'referal_system')
profile_keyboard.add(btn2, btn3, btn1, btn4)


#количество мин
mines_kolv_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width = 3)
mines_kolv_keyboard.add('3', '5', '10', '15', '20', '24', 'Отмена')


def favorite_games_keyboard(us_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    favorite_games_buttons = types.InlineKeyboardMarkup(row_width = 2)
    cursor.execute('SELECT favorite_cube, favorite_bouling, favorite_backetball, favorite_dartc, favorite_football, favorite_avtomat, favorite_blackjack FROM apple WHERE user_id = (?)', (us_id,))
    favorite_game = cursor.fetchone()
    btn1 = types.InlineKeyboardButton(text = '🎲 Кубик', callback_data = 'cube')
    btn2 = types.InlineKeyboardButton(text = '🎳 Боулинг', callback_data = 'bouling')
    btn3 = types.InlineKeyboardButton(text = '🏀 Баскетбол', callback_data = 'backetball')
    btn4 = types.InlineKeyboardButton(text = '🎯 Дартс', callback_data = 'dartc')
    btn5 = types.InlineKeyboardButton(text = '⚽ Футбол', callback_data = 'football')
    btn6 = types.InlineKeyboardButton(text = '🎰 Автомат', callback_data = 'avtomat')
    btn7 = types.InlineKeyboardButton(text = '♥️♠️ BlackJack', callback_data = 'BlackJack')
    btn8 = types.InlineKeyboardButton(text = '◀️ Назад', callback_data = 'menu')
    btn9 = types.InlineKeyboardButton(text = '🎮 Список игр', callback_data = 'spisok_pvp')
    listok = []
    if favorite_game[0] == 1:
        listok.append(btn1)
    if favorite_game[1] == 1:
        listok.append(btn2)
    if favorite_game[2] == 1:
        listok.append(btn3)
    if favorite_game[3] == 1:
        listok.append(btn4)
    if favorite_game[4] == 1:
        listok.append(btn5)
    if favorite_game[5] == 1:
        listok.append(btn6)
    if favorite_game[6] == 1:
        listok.append(btn7)
    favorite_games_buttons.add(*listok)
    favorite_games_buttons.add(btn9)
    favorite_games_buttons.add(btn8)
    return favorite_games_buttons

#список игр куб
def list_cube_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_cube_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_cube')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'cube')
    btn3 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_cube')
    btn4 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_cube") 
    list_cube_buttons.add(btn1, btn2)
    list_cube_buttons.add(btn3, btn5)
    cursor.execute('SELECT * FROM list_game_cube')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🎲 Игрок {row[1]} | {row[2]} RUB', callback_data=f'cubgame_{row[0]}')
        list_cube_buttons.add(button_list)
    list_cube_buttons.add(btn4)
    return list_cube_buttons

#список игр боулинг
def list_bouling_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_bouling_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_bouling')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'bouling')
    btn4 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_bouling')
    btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_bouling")   
    list_bouling_buttons.add(btn1, btn2)
    list_bouling_buttons.add(btn4, btn5)
    cursor.execute('SELECT * FROM list_game_bouling')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🎳 Игрок {row[1]} | {row[2]} RUB', callback_data=f'boulinggame_{row[0]}')
        list_bouling_buttons.add(button_list)
    list_bouling_buttons.add(btn3)
    return list_bouling_buttons

#список игр баскет
def list_backetball_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_backetball_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_backetball')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'backetball')
    btn4 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_backetball')
    btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_backetball")   
    list_backetball_buttons.add(btn1, btn2)
    list_backetball_buttons.add(btn4, btn5)
    cursor.execute('SELECT * FROM list_game_backetball')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🏀 Игрок {row[1]} | {row[2]} RUB', callback_data=f'backetballgame_{row[0]}')
        list_backetball_buttons.add(button_list)
    list_backetball_buttons.add(btn3)
    return list_backetball_buttons

#список игр дартс
def list_dartc_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_dartc_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_dartc')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'dartc')
    btn4 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_dartc')
    btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_dartc")   
    list_dartc_buttons.add(btn1, btn2)
    list_dartc_buttons.add(btn4, btn5)
    cursor.execute('SELECT * FROM list_game_dartc')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🎯 Игрок {row[1]} | {row[2]} RUB', callback_data=f'dartcgame_{row[0]}')
        list_dartc_buttons.add(button_list)
    list_dartc_buttons.add(btn3)
    return list_dartc_buttons

#список игр футбол
def list_football_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_football_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_football')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'football')
    btn4 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_football')
    btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_football")   
    list_football_buttons.add(btn1, btn2)
    list_football_buttons.add(btn4, btn5)
    cursor.execute('SELECT * FROM list_game_football')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'⚽ Игрок {row[1]} | {row[2]} RUB', callback_data=f'footballgame_{row[0]}')
        list_football_buttons.add(button_list)
    list_football_buttons.add(btn3)
    return list_football_buttons

#список игр автомат
def list_avtomat_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_avtomat_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_avtomat')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'avtomat')
    btn4 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_avtomat')
    btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_avtomat")   
    list_avtomat_buttons.add(btn1, btn2)
    list_avtomat_buttons.add(btn4, btn5)
    cursor.execute('SELECT * FROM list_game_avtomat')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🎰 Игрок {row[1]} | {row[2]} RUB', callback_data=f'avtomatgame_{row[0]}')
        list_avtomat_buttons.add(button_list)
    list_avtomat_buttons.add(btn3)
    return list_avtomat_buttons

#Cписок игр блэкджэк
def list_blackjack_buttons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    list_blackjack_buttons = types.InlineKeyboardMarkup(row_width = 2)
    btn1 = InlineKeyboardButton(text = '🎮 Создать игру', callback_data = 'create_game_bj')
    btn2 = InlineKeyboardButton(text = '🔄 Обновить', callback_data = 'BlackJack')
    btn3 = InlineKeyboardButton(text = '🤖 Играть с ботом', callback_data = 'bot_bj')
    btn4 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
    btn5 = InlineKeyboardButton(text = '⭐️ В избранное', callback_data = "add_favorite_blackjack")   
    list_blackjack_buttons.add(btn1, btn2)
    list_blackjack_buttons.add(btn3, btn5)
    ses = 0
    cursor.execute(f'SELECT * FROM list_game_blackjack WHERE player2 = {0}')
    a = cursor.fetchall()
    for row in a:
        button_list = types.InlineKeyboardButton(text=f'🃏 Игрок {row[1]} | {row[2]} RUB', callback_data=f'bjgame_{row[0]}')
        list_blackjack_buttons.add(button_list)
    list_blackjack_buttons.add(btn4)
    return list_blackjack_buttons


#Помощь суммы ставок
def stavka_keyboard(us_id):
    stavka_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width = 2)
    stavka_keyboard.add('Отмена')
    return stavka_keyboard

#Помощь реквизитов
def rekvizit_keyboard(us_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT last_rekvizit FROM apple WHERE user_id = {us_id}")
    rekvizit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rekvizit = cursor.fetchone()[0]
    if rekvizit != None:
        rekvizit_keyboard.add(f'{rekvizit}')
    return rekvizit_keyboard


