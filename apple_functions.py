import telebot
import sqlite3
import time
import requests
import random
import json
import requests
from blackjack import blackjack_map
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from apple_keyboard import menu_keyboard, game_keyboard, apple_keyboard_start, apples_map, triple_keyboard, triple_map, admin_keyboard, nazad, setting_kassa, otmena_keyboard, hideBoard, deposit_btn, sogl_keyboard, vivod_keyboard, close_message_keyboard, profile_keyboard, mines_keyboard, mines_map
from config import admin, token, chats, link_chat, news_link, admin_link
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(token)

#Регистрация
def db_table_val (user_id: int, username: str, priglasil_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"select count(*) from apple where user_id = {user_id}")
    if username != None:
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO apple (user_id, username, priglasil_id) VALUES (?,?,?)', (user_id, username, priglasil_id,))
            conn.commit()
            bot.send_message(user_id,f"🎉Привет игрок!\n\n"
                             f"Политика и условия пользования данным ботом.\n"
                             f"1. Играя у нас, вы берёте все риски за свои средства на себя.\n"
                             f"2. Принимая правила, Вы подтверждаете своё совершеннолетие!\n"
                             f"3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!\n"
                             f"4. Мультиаккаунты запрещены!\n"
                             f"5. Скрипты, схемы использовать запрещено!\n"
                             f"6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n\n"
                             f"Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием! Вывод денежных средств осуществляется в течении 24ч! По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам играм обогащайтесь в поддержку, указанную в описании к боту. Пишите сразу по делу, а не «Здравствуйте! Тут?»\n"
                             f"Старайтесь изложить свои мысли четко и ясно, что поддержка не мучалась и не пыталась Вас понять.\n"
                             f"Спасибо за понимание!\n\n",
                             reply_markup = sogl_keyboard)
            if priglasil_id !=None:
                ops = 0.2
                cursor.execute('UPDATE apple SET referal_all = referal_all + 1 WHERE user_id = (?)', (priglasil_id,))
                cursor.execute(f'UPDATE apple SET balance = balance + {ops} WHERE user_id = (?)', (priglasil_id,))
                cursor.execute(f'UPDATE apple SET referal_money = referal_money + {ops} WHERE user_id = (?)', (priglasil_id,))
                conn.commit()
                bot.send_message(priglasil_id, text = f'🙎🏼‍♂️ У вас новый реферал - {username}!\n🪃 Вы получил 0.20 RUB\n🪃Также вы будете получать 5% от его пополнений')
        else:
            glav_message(user_id)
    else:
        bot.send_message(user_id, '⚠️ Установите username (имя пользователя) в Telegram\nСделать это можно во вкладке "Настройки" - "Выбрать имя пользователя" и перезапустите бота - нажмите /start')


def func_add_favorite(call, game_name):
    us_id = call.from_user.id
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'SELECT favorite_{game_name} FROM apple WHERE user_id = (?)', (us_id,))
    favorit_game = cursor.fetchone()[0]
    if favorit_game == 0:
        cursor.execute(f'UPDATE apple SET favorite_{game_name} = 1 WHERE user_id = {us_id}')
        conn.commit()
        bot.answer_callback_query(callback_query_id= call.id,text =  "✅ Добавлено в избранное",show_alert = True)
    if favorit_games == 1:
        cursor.execute(f'UPDATE apple SET favorite_{game_name} = 0 WHERE user_id = {us_id}')
        conn.commit()
        bot.answer_callback_query(callback_query_id= call.id, text = "❌ Удалено из избранное",show_alert = True)





def get_username(message):
    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM apple WHERE user_id = (?)', (message.from_user.id,))
        us_name = cursor.fetchone()
        if message.from_user.username == None or us_name[0] == None:
            bot.send_message(call.from_user.id, text = 'Установите username для корректной работы бота и пропишите /start')
            return False



        if us_name[0] != message.from_user.username:
            cursor.execute('UPDATE apple SET username = (?) WHERE user_id = (?)', (message.from_user.username, message.from_user.id,))
            conn.commit()
            return True
        else:
            return True
    except:
        bot.send_message(message.from_user.id, text = 'Установите username для корректной работы бота и пропишите /start')
        return False


def get_usernamecall(call):
    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM apple WHERE user_id = (?)', (call.from_user.id,))
        us_name = cursor.fetchone()[0]
        if call.from_user.username == None:
            bot.send_message(call.from_user.id, text = 'Установите username для корректной работы бота и пропишите /start')
            return False
        if us_name != call.from_user.username:
            cursor.execute('UPDATE apple SET username = (?) WHERE user_id = (?)', (call.from_user.username, call.from_user.id,))
            conn.commit()
            return True
        else:
        	return True
    except:
        bot.send_message(call.from_user.id, text = 'Установите username для корректной работы бота и пропишите /start')
        return False

#Меню
def glav_menu(us_id):
    balance = get_user_balance(us_id)
    bot.send_message(us_id, text = 'Главное меню',reply_markup=hideBoard)
    bot.send_photo(us_id, photo = 'https://imgur.com/lv6SX8L', caption = f"<b>🎉 Добро пожаловать!\n💰 Ваш баланс: {balance} RUB</b>", reply_markup=menu_keyboard(us_id), parse_mode = 'HTML')

def glav_message(us_id):
    balance = get_user_balance(us_id)
    bot.send_photo(us_id, photo = 'https://imgur.com/lv6SX8L', caption = f"<b>🎉 Добро пожаловать!\n💰 Ваш баланс: {balance} RUB</b>", reply_markup=menu_keyboard(us_id), parse_mode = 'HTML')

def profile(us_id,name):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT all_win FROM apple WHERE user_id = ('%s')"%(us_id))
    all_win = round(cursor.fetchone()[0], 2)
    cursor.execute("SELECT all_lose FROM apple WHERE user_id = ('%s')"%(us_id))
    all_lose = cursor.fetchone()[0]
    cursor.execute("SELECT all_game_apple FROM apple WHERE user_id = ('%s')"%(us_id))
    all_game_apple = cursor.fetchone()[0]
    cursor.execute("SELECT all_game_triple FROM apple WHERE user_id = ('%s')"%(us_id))
    all_game_triple = cursor.fetchone()[0]
    cursor.execute("SELECT all_game_mines FROM apple WHERE user_id = ('%s')"%(us_id))
    all_game_mines = cursor.fetchone()[0]
    cursor.execute("SELECT how_deposit FROM apple WHERE user_id = ('%s')"%(us_id))
    deposit = cursor.fetchone()[0]
    cursor.execute("SELECT how_vivod FROM apple WHERE user_id = ('%s')"%(us_id))
    vivod = cursor.fetchone()[0]
    cursor.execute("SELECT game_win FROM apple WHERE user_id = ('%s')"%(us_id))
    game_win = cursor.fetchone()[0]
    cursor.execute("SELECT game_lose FROM apple WHERE user_id = ('%s')"%(us_id))
    game_lose = cursor.fetchone()[0]

    balance = get_user_balance(us_id)
    bot.send_photo(us_id, photo = 'https://imgur.com/wc7Jddd', caption =  f"➖➖➖➖➖➖➖➖\n🙎‍♂️ Имя: <code>{name}</code>\n🌑 ID: <code>{us_id}</code>\n➖➖➖➖➖➖➖➖\n🏆 Выиграно игр - {game_win}\n💣 Проиграно игр -{game_lose}\n➖➖➖➖➖➖➖➖\n💰 Баланс: {balance} RUB\n➖➖➖➖➖➖➖➖", reply_markup=profile_keyboard,parse_mode = 'HTML')

def stats(us_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    #cursor.execute("SELECT COUNT(1) FROM apple")
    #all_users = cursor.fetchone()[0]
    #cursor.execute("SELECT SUM(`game_win`) FROM apple")
    #game_win = cursor.fetchone()[0]
    #cursor.execute("SELECT SUM(`game_lose`) FROM apple")
    #game_lose = cursor.fetchone()[0]
    #cursor.execute("SELECT SUM(`all_win`) FROM apple")
    #all_win = cursor.fetchone()[0]
    #cursor.execute("SELECT SUM(`all_lose`) FROM apple")
    #all_lose = cursor.fetchone()[0]
    #cursor.execute("SELECT all_vivod FROM settings WHERE bot = 1")
    #vivod = cursor.fetchone()[0]

    keys = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text = '💬 Чат', url = link_chat)
    btn2 = types.InlineKeyboardButton(text = '👨‍💻 Админ', url = admin_link)
    btn3 = types.InlineKeyboardButton(text = '🗞 Новости', url = news_link)
    btn4 = types.InlineKeyboardButton(text = '🏆 Топ рефоводов', callback_data = 'bas')
    btn5 = types.InlineKeyboardButton(text = '📥 Топ выводов', callback_data = 'top_vivod')
    btn6 = types.InlineKeyboardButton(text = '🤑 Топ выигрышей', callback_data = 'top_win')

    keys.add(btn1,btn2,btn3)
    keys.add(btn6)
    keys.add(btn5, btn4)
    bot.send_photo(us_id,photo = 'https://imgur.com/lv6SX8L', caption = f'📋 <b>Выберите нужный пункт</b>', reply_markup = keys, parse_mode = 'HTML')


def adminka(message, admin):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  us_id = message.from_user.id
  if admin == 1:
    if message.text == 'Изменить мин. ставку':
      cursor.execute("SELECT min_stavka FROM settings WHERE bot = 1")
      now_min_stavka = cursor.fetchone()[0]
      bot.send_message(us_id, text=f'Сейчас минимальная ставка состовляет {now_min_stavka}, введите новое значение', reply_markup = nazad)
      bot.register_next_step_handler(message, new_min_stavka)

    if message.text == 'Сделать рассылку':
      msg = bot.send_message(us_id, text='Введите текст рассылки, разметки для текста:\n\n<b>Ваш текст</b> - Жирный\n\n<i>Ваш текст</i> - Курсив\n\n<code>Ваш текст</code> - Копируемый в клик\n\n<u>Ваш текст</u> -Подчеркнутый\n\n<a href="Ваша ссылка">Ваш Текст</a> - Ссылка в слове/предложении', reply_markup = nazad )
      bot.register_next_step_handler(msg, rassilka)

    if message.text == 'Выдать/Забрать баланс':
      bot.send_message(us_id, text='Введите username пользователя', reply_markup = nazad)
      bot.register_next_step_handler(message, get_balance)

    if message.text == 'Настройки кассы':
      bot.send_message(us_id, text='Выберите опцию',reply_markup=setting_kassa)

    if message.text == 'Снять кассу':
      cursor.execute("UPDATE settings SET kassa = ('%s') WHERE bot = 1"%(0,))
      conn.commit()
      bot.send_message(us_id, text='Касса снята!', reply_markup = nazad)

    if message.text == 'Изменить антиминус':
      cursor.execute("SELECT antiminus FROM settings WHERE bot = 1")
      antiminus = cursor.fetchone()[0]
      bot.send_message(us_id, text=f'Сейчас антиминус составляет {antiminus}, введите новое значение', reply_markup = nazad)
      bot.register_next_step_handler(message,new_antiminus)

    if message.text == 'В меню':
      bot.register_next_step_handler(message, glav_menu)

    if message.text == 'Назад':
      bot.send_message(us_id, text='Меню админа', reply_markup = admin_keyboard)

#Админка
def adminka_menu(message):
    try:
        us_id = message.from_user.id
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT admin FROM apple WHERE user_id = ('%s')"%(us_id))
        admin = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(1) FROM apple")
        all_users = cursor.fetchone()[0]
        cursor.execute("SELECT all_deposit FROM settings WHERE bot = ('%s')"%(1,))
        all_deposit = round(cursor.fetchone()[0], 2)
        cursor.execute("SELECT kassa FROM settings WHERE bot = ('%s')"%(1,))
        kassa = round(cursor.fetchone()[0], 2)
        cursor.execute("SELECT pvp_money FROM settings WHERE bot = ('%s')"%(1,))
        pvp_money = round(cursor.fetchone()[0], 2)
        cursor.execute("SELECT SUM(`game_win`) FROM apple")
        game_win = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(`game_lose`) FROM apple")
        game_lose = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(`all_win`) FROM apple")
        all_win = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(`all_lose`) FROM apple")
        all_lose = cursor.fetchone()[0]
        cursor.execute("SELECT all_vivod FROM settings WHERE bot = 1")
        vivod = cursor.fetchone()[0]
        if admin == 1:
            bot.send_message(us_id, text=f'📊 <b>Cтатистика проекта:</b>\n\n➖➖➖➖➖➖➖➖\n👨‍💻 Число пользователей: {all_users}\n💵 Внесено средств: {all_deposit}\n📤 Выплачено {vivod} RUB\n➖➖➖➖➖➖➖➖\n🏦 Касса проекта: {kassa} RUB\n🏦 Выручка с комиссий сегодня: {pvp_money} RUB\n➖➖➖➖➖➖➖➖\n🏆 Выиграно игр: {game_win} шт ({all_win} RUB)\n💣 Проиграно игр: {game_lose} шт ({all_lose} RUB)\n➖➖➖➖➖➖➖➖ ', reply_markup = admin_keyboard, parse_mode = 'HTML')
            bot.register_next_step_handler(message, adminka, admin)
    except Exception as e:
      bot.send_message(us_id, e)

#Вывод сумма
def vivod_sum(message):
    us_id = message.from_user.id
    try:
        if int(message.text) >= 30:
            summa = int(message.text)
            bot.send_message(us_id, text=f"Выберите способ вывода", reply_markup=vivod_keyboard())
            bot.register_next_step_handler(message,vivod_rekv,summa)
        else:
            bot.send_message(us_id, text=f"Минимальная сумма - 30р", reply_markup=menu_keyboard(us_id))
    except:
        bot.send_message(us_id, text=f"Введите число!", reply_markup=menu_keyboard(us_id))

def vivod_rekv(message, summa):
    us_id = message.from_user.id
    sposob = message.text
    bot.send_message(us_id, text=f"Введите реквизиты:", reply_markup=vivod_keyboard())
    bot.register_next_step_handler(message, vivod, sposob, summa)


def get_all_users(priglasil_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'''SELECT user_id FROM apple ''')
    row = cursor.fetchall()
    for user in row:
        user = user[0]
        if priglasil_id == user:
            return priglasil_id
        else:
            pass







#Получение ставки
def get_stavka(message, game_name, rg = 0):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor() # - Обработчик ставок
    us_id = message.from_user.id
    balance = get_user_balance(us_id)
    cursor.execute("SELECT min_stavka FROM settings WHERE bot = ('%s')"%(1,))
    min_stavka = cursor.fetchone()[0]
    cursor.execute("SELECT max_stavka FROM settings WHERE bot = ('%s')"%(1,))
    max_stavka = cursor.fetchone()[0]
    if message.text.isdigit():
        if int(message.text) <= balance:
            if int(message.text)>= min_stavka:
              if int(message.text)<=max_stavka:
                cursor.execute("UPDATE apple SET game_status = 1 WHERE user_id = (?)", (us_id,))
                stavka = message.text
                stavka = int(stavka)
                if game_name == 'apple':
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    msg = bot.send_message(us_id, text=f"Игра началсь!", reply_markup=hideBoard)
                    bot.send_photo(us_id, photo = 'https://imgur.com/zDZBsIj',caption=f"🍏 Текущий выйгрыш- {stavka} RUB (x1)\n\n🍎 Следущий выйгрыш: {stavka *1.25} RUB (x1.25)", reply_markup=apple_keyboard_start)
                    bot.delete_message(chat_id=us_id, message_id=msg.message_id)
                    cursor.execute("UPDATE apple SET all_game_apple = all_game_apple + 1 WHERE user_id = ('%s')"%(us_id,))
                    conn.commit()
                    func_apple_map(user_id=us_id, apples_map=apples_map, now_state=1, now_x=1.25, now_stavka=stavka, win_money = stavka)
                if game_name == 'triple':
                    conn.close()
                    func_triple_map(user_id=us_id, triple_map=triple_map, now_stavka=stavka)
                    msg = bot.send_message(us_id, text=f"Игра началсь!", reply_markup=hideBoard)
                    bot.send_photo(us_id, photo = 'https://imgur.com/7tCq3Go', caption=f"💰 Ваша ставка: {stavka}", reply_markup=triple_keyboard)
                    bot.delete_message(chat_id=us_id, message_id=msg.message_id)
                if game_name == 'mines':
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_photo(us_id, photo = 'https://imgur.com/7QT9M4p', caption=f"💰 Ваша ставка: {stavka}", reply_markup=mines_keyboard)
                    cursor.execute("UPDATE apple SET all_game_mines = all_game_mines + 1 WHERE user_id = ('%s')"%(us_id,))
                    conn.commit()
                    func_mines_map(user_id = us_id, mines_map=mines_map, now_stavka = stavka, now_x = 1, now_state = 0, win_money = stavka)
                if game_name == 'blackjack':
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🃏 Новая игра (BLACKJACK)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_blackjack(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)


                if game_name == 'cube' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🎲 Новая игра (КУБ)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_cube(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)

                if game_name == 'bouling' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🎳 Новая игра (БОУЛИНГ)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_bouling(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)
                if game_name == 'bouling' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_bouling(us_id = us_id, stavka = stavka)

                if game_name == 'backetball' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🏀 Новая игра (БАСКЕТБОЛ)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_backetball(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)
                if game_name == 'backetball' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_backetball(us_id = us_id, stavka = stavka)

                if game_name == 'dartc' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🎯 Новая игра (ДАРТС)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_dartc(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)
                if game_name == 'dartc' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_dartc(us_id = us_id, stavka = stavka)

                if game_name == 'football' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"⚽️ Новая игра (ФУТБОЛ)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_football(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)
                if game_name == 'football' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_football(us_id = us_id, stavka = stavka)

                if game_name == 'avtomat' and rg == 0:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    bot.send_message(us_id, text = "Игра создана!\nВы получите уведомление когда к вам присоеденится игрок", reply_markup = menu_keyboard(us_id))
                    msg = bot.send_message(chats, text = f"🎰 Новая игра (АВТОМАТ)!\nИгрок: @{message.from_user.username}\nСтавка: {stavka} RUB ")
                    func_create_avtomat(username = message.from_user.username,us_id = us_id, stavka = stavka, message_id = msg.message_id)
                if game_name == 'avtomat' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_avtomat(us_id = us_id, stavka = stavka)
                if game_name == 'bj' and rg == 1:
                    cursor.execute(f'UPDATE apple SET balance = balance - {stavka} where user_id = ?', [us_id])
                    conn.commit()
                    func_bot_blackjack(us_id = us_id, stavka = stavka)

              else:
                bot.send_message(us_id, text=f"Максимальная ставка - {max_stavka} руб", reply_markup=menu_keyboard(us_id))

            else:
                bot.send_message(us_id, text=f"Минимальная ставка - {min_stavka} руб", reply_markup=menu_keyboard(us_id))
        else:
            bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
    else:
        glav_message(us_id)
             




#Игры с ботом
def func_start_bot_game(us_id, game_name):
    if game_name == 'cube':
        func_bot_cube(us_id)
    if game_name == 'bj':
        func_bot_blackjack(us_id)
    if game_name == 'bouling':
        func_bot_bouling(us_id)
    if game_name == 'backetball':
        func_bot_backetball(us_id)
    if game_name == 'football':
        func_bot_football(us_id)
    if game_name == 'dartc':
        func_bot_dartc(us_id)
    if game_name == 'avtomat':
        func_bot_avtomat(us_id)


def func_bot_blackjack(us_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    bot_score = random.randint(15, 26)
    key = random.choice(list(blackjack_map.keys()))
    value = random.choice(list(blackjack_map.values()))
    link = blackjack_map.get(key)
    link = random.choice(list(link.values()))
    key2 = random.choice(list(blackjack_map.keys()))
    value2 = random.choice(list(blackjack_map.values()))
    link2 = blackjack_map.get(key2)
    link2 = random.choice(list(link2.values()))
    if key == 11 and key2 == 11:
      res = 21
    else:
      res = int(key) + int(key2)
    cursor.execute(f'UPDATE apple SET bj_score_for_bot = {bot_score} WHERE user_id = {us_id}')
    cursor.execute(f'UPDATE apple SET bj_score_for_user = {res} WHERE user_id = {us_id}')
    conn.commit()
    bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
    btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'eshebot_bj{us_id}')
    btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stopbot_bj{us_id}')
    bj_btn.add(btn1, btn2)
    bot.send_photo(us_id, photo = open('bj_image/' + link, 'rb'), reply_markup = hideBoard)
    bot.send_photo(us_id, photo = open('bj_image/' +link2, 'rb'))
    bot.send_message(us_id, text = f'🤖 Бот решил остановится и ждет вас')
    time.sleep(0.3)
    bot.send_message(us_id, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )

def func_bot_cube (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '🎲')
  time.sleep(5)
  bot.send_message(us_id, f'🎲 Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '🎲')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'🎲 Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'🎲 Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'🎲 Боту выпало число {bsg.dice.value}\n⚪️ Ничья!', reply_markup=menu_keyboard(us_id))

def func_bot_bouling (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '🎳')
  time.sleep(5)
  bot.send_message(us_id, f'🎳 Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '🎳')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'🎳 Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'🎳 Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'🎳 Боту выпало число {bsg.dice.value}\n⚪️ Ничья!', reply_markup=menu_keyboard(us_id))
def func_bot_backetball (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '🏀')
  time.sleep(5)
  bot.send_message(us_id, f'🏀 Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '🏀')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'🏀 Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'🏀 Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'🏀 Боту выпало число {bsg.dice.value}\n⚪️ Ничья!', reply_markup=menu_keyboard(us_id))

def func_bot_dartc (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '🎯')
  time.sleep(5)
  bot.send_message(us_id, f'🎯 Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '🎯')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'🎯 Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'🎯 Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'🎯 Боту выпало число {bsg.dice.value}\n⚪️ Ничья!')

def func_bot_football (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '⚽️')
  time.sleep(5)
  bot.send_message(us_id, f'⚽️ Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '⚽️')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'⚽️ Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'⚽️ Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'⚽️ Боту выпало число {bsg.dice.value}\n⚪️ Ничья!', reply_markup=menu_keyboard(us_id))

def func_bot_avtomat (us_id):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  usg = bot.send_dice(us_id, '🎰')
  time.sleep(5)
  bot.send_message(us_id, f'🎰 Вам выпало число {usg.dice.value}')
  bsg = bot.send_dice(us_id, '🎰')
  time.sleep(5)
  if usg.dice.value > bsg.dice.value:
    bot.send_message(us_id, f'🎰 Боту выпало число {bsg.dice.value}\n🟢 Вы выиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value < bsg.dice.value:
    bot.send_message(us_id, f'🎰 Боту выпало число {bsg.dice.value}\n🔴 Вы проиграли!', reply_markup=menu_keyboard(us_id))
  if usg.dice.value == bsg.dice.value:
    bot.send_message(us_id, f'🎰 Боту выпало число {bsg.dice.value}\n⚪️ Ничья!', reply_markup=menu_keyboard(us_id))


#Генерация карты яблок
def func_apple_map(user_id: int, apples_map, now_state: int, now_x: int, now_stavka: int, win_money: int):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  mapa = json.dumps(apples_map)

  cursor.execute('UPDATE apple SET map_buttons = ? where user_id = ?', (mapa,user_id))
  cursor.execute('UPDATE apple SET now_state = ? where user_id = ?', (now_state,user_id))
  cursor.execute('UPDATE apple SET now_x = ? where user_id = ?', (now_x,user_id))
  cursor.execute('UPDATE apple SET now_stavka = ? where user_id = ?', (now_stavka,user_id))
  cursor.execute('UPDATE apple SET win_money = ? where user_id = ?', (win_money,user_id))
  conn.commit()

#Генерация карты трипл
def func_triple_map (user_id: int, triple_map, now_stavka: int):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  mapa = json.dumps(triple_map)
  cursor.execute('UPDATE apple SET triple_map_buttons = ? where user_id = ?', (mapa,user_id))
  cursor.execute('UPDATE apple SET now_stavka = ? where user_id = ?', (now_stavka,user_id))
  conn.commit()


#Генерация карты мин
def func_mines_map(user_id: int, mines_map, now_stavka: int, now_x: int, now_state: int, win_money: int):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    mapa = json.dumps(mines_map)
    cursor.execute('UPDATE apple SET mines_map_buttons = ? where user_id = ?', (mapa,user_id))
    cursor.execute('UPDATE apple SET now_stavka = ? where user_id = ?', (now_stavka,user_id))
    cursor.execute('UPDATE apple SET now_x = ? where user_id = ?', (now_x, user_id))
    cursor.execute('UPDATE apple SET now_state = ? where user_id = ?', (now_state, user_id))
    cursor.execute('UPDATE apple SET win_money = ? where user_id = ?', (win_money,user_id))
    conn.commit()

def func_create_cube(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_cube VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()

def func_create_blackjack(username, us_id, stavka: int, message_id, player2 = 0, score = 0):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_blackjack VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (glkey, username, stavka, us_id, message_id, player2, score, score, score, score))
    conn.commit()

def func_create_bouling(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_bouling VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()

def func_create_backetball(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_backetball VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()

def func_create_dartc(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_dartc VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()

def func_create_football(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_football VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()

def func_create_avtomat(username, us_id, stavka: int, message_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    glkey = random.randint(1111111, 9999999)
    mapa = {glkey : {username: stavka}}
    cursor.execute('INSERT INTO list_game_avtomat VALUES (? , ? , ?, ?, ?)', (glkey, username, stavka, us_id, message_id))
    conn.commit()


#генерация платежного id
def generate_qid():
    qid = random.randint(1111111, 9999999)
    return qid

#Получить баланс
def get_user_balance(id):
    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(f'''SELECT balance FROM apple WHERE user_id = '{id}' ''')
        balance = round(cursor.fetchone()[0], 2)
        return balance
    except:
        pass

#Получить статус админки
def get_admin_status(us_id):
    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT admin FROM apple WHERE user_id = ('%s')"%(us_id))
        admin = cursor.fetchone()[0]
        return admin
    except:
        pass
# Платежка пеер
def payeer(message):
  us_id = message.from_user.id
  #try:
  summa = int(message.text)
  if summa >= 10:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        #cursor.execute("SELECT crystal_key FROM settings WHERE bot = 1")
        #key = cursor.fetchone()[0]
        #cursor.execute("SELECT crystal_login FROM settings WHERE bot = 1")
        #login =cursor.fetchone()[0]
        values = {
        'account':'P1064634299',
        'apiId':'1586752726',
        'apiPass':'M4LgA6Smkt7tZRrh'}

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url = 'https://payeer.com/ajax/api/api.php', data=values, headers=headers)
        response.encoding = 'utf-8'

        print (response.content)
        #json_response = response.json()
        #url = json_response['url']
        #ids = json_response['id']
        #cursor.execute('UPDATE apple SET pay_id = (?) where user_id = (?)', (ids, us_id))
        #conn.commit()
        #btn_list = types.InlineKeyboardMarkup(row_width = 1)
        #btn1 = InlineKeyboardButton(text = '💸 Перейти к оплате', url = url)
        #btn2 = InlineKeyboardButton(text = '🔄 Проверить оплату', callback_data = f'check_payeer_{summa}')
        #btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'back_popol')
        #btn_list.add(btn1,btn2,btn3)
        #bot.send_photo(us_id, photo = 'https://sun9-74.userapi.com/impg/kLo0xGJaA9ldITqLhaJ43qajbEpX5c1ycFw-wg/JyojAiFErCs.jpg?size=1000x400&quality=96&sign=594cab719193d6bf0043067dacd5fddc&type=album',caption = f'Cчёт действителен 60 мин!\nCсылка для оплаты:\n{url}', reply_markup = btn_list)
 # except:
    #bot.send_message(us_id,f'Введите число!', reply_markup = menu_keyboard(us_id))

# Платежка кристал
def crystal_pay(message):
  us_id = message.from_user.id
  try:
    summa = int(message.text)
    if summa >= 10:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT crystal_key FROM settings WHERE bot = 1")
        key = cursor.fetchone()[0]
        cursor.execute("SELECT crystal_login FROM settings WHERE bot = 1")
        login =cursor.fetchone()[0]
        response = requests.get(url = f'https://api.crystalpay.ru/v1/?s={key}&n={login}&o=receipt-create&amount={summa}&lifetime=60')
        json_response = response.json()
        url = json_response['url']
        ids = json_response['id']
        cursor.execute('UPDATE apple SET pay_id = (?) where user_id = (?)', (ids, us_id))
        conn.commit()
        btn_list = types.InlineKeyboardMarkup(row_width = 1)
        btn1 = InlineKeyboardButton(text = '💸 Перейти к оплате', url = url)
        btn2 = InlineKeyboardButton(text = '🔄 Проверить оплату', callback_data = f'check_crystal_{summa}')
        btn3 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'back_popol')
        btn_list.add(btn1,btn2,btn3)
        bot.send_photo(us_id, photo = 'https://imgur.com/1xT6uHl',caption = f'Cчёт действителен 60 мин!\nCсылка для оплаты:\n{url}', reply_markup = btn_list)
  except:
    bot.send_message(us_id,f'Введите число!', reply_markup = menu_keyboard(us_id))
# Платежка QIWI P2P
def qiwip2p(message):
    us_id = message.from_user.id
    try:
        pay = int(message.text)
        if pay >= 10:
            us_id = message.from_user.id
            qid = generate_qid()
            conn = sqlite3.connect('database.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT p2p_key FROM settings WHERE bot = 1")
            KEY = cursor.fetchone()[0]
        #KEY = json.loads(KEY[0])
            cursor.execute('UPDATE apple SET pay_id = (?) where user_id = (?)', (qid, us_id))
            cursor.execute('UPDATE apple SET pay_sum = (?) where user_id = (?)', (pay, us_id))
            conn.commit()
            p2p = QiwiP2P(auth_key=KEY)

            new_bill = p2p.bill(bill_id=qid, amount=pay, lifetime=30, comment = "casino bot")#, customFields={'themeCode': 'Uliana-AVVHLGyhXI'})
            bot.send_photo(us_id, photo = 'https://imgur.com/1xT6uHl',caption = f'Cчёт действителен 30 мин!\nCсылка для оплаты:\n{new_bill.pay_url}', reply_markup = deposit_btn)
        else:
            bot.send_message(us_id,f'Минимальная сумма пополнения 10 RUB', reply_markup = menu_keyboard(us_id))
    except:
        bot.send_message(us_id,f'Введите число!', reply_markup = menu_keyboard(us_id))
#QIWI key
def new_qiwikey(message):
    if message.text != 'Админка':
        try:
            conn = sqlite3.connect('database.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE settings set p2p_key = (?) WHERE bot = 1", (message.text,))
            conn.commit()
            bot.send_message(message.from_user.id, f'Ключ изменен!')
        except Exception as e:
            bot.send_message(message.from_user.id, f'Ошибка\n{e}')
    else:
        adminka_menu(message)
      




def zero_game(message):
    us_id = message.from_user.id
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    username = message.text[1:]
    try:
        cursor.execute(f'''UPDATE apple SET game_status = 0 WHERE username = '{username}' ''')
        conn.commit()
        bot.send_message(us_id, text = 'Успешно!', reply_markup = admin_keyboard)
    except:
        bot.send_message(us_id, text = 'Такого пользователя не существует', reply_markup = admin_keyboard)



#Рассылка
def rassilka(message):
    us_id = message.from_user.id
    if message.text == 'Админка':
        adminka_menu(message)
    else:
        rassilka = message.text
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(f'''SELECT user_id FROM apple ''')
        row = cursor.fetchall()
        bot.send_message(us_id, text = "Рассылка началась!",reply_markup=admin_keyboard)
        succ = 0
        unsucc = 0
        for user in row:
            try:
                bot.send_message(user[0], f"{rassilka}",reply_markup=close_message_keyboard, parse_mode="HTML")
                succ = succ+1
            except:
                unsucc = unsucc + 1
            
        bot.send_message(us_id, text = f'Рассылка завершена!\nОтправлено: {succ}\nНе отправленно: {unsucc}',reply_markup=admin_keyboard)


#Пополнение баланса


#Установка мин ставки
def new_min_stavka(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    if message.text == 'Админка':
        adminka_menu(message)
    else:
        new_min_stavka = message.text
        try:
            new_min_stavka = int(new_min_stavka)
            cursor.execute("UPDATE settings SET min_stavka = ('%s') WHERE bot = 1"%(new_min_stavka,))
            conn.commit()
            bot.send_message(us_id,f'Минимальная ставка теперь {new_min_stavka}', reply_markup=admin_keyboard)
        except:
            bot.send_message(us_id,f'Введите число!', reply_markup=admin_keyboard)

def new_max_stavka(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    if message.text == 'Админка':
        adminka_menu(message)
    else:
        new_max_stavka = message.text
        try:
            new_max_stavka = int(new_max_stavka)
            cursor.execute("UPDATE settings SET max_stavka = ('%s') WHERE bot = 1"%(new_max_stavka,))
            conn.commit()
            bot.send_message(us_id,f'Минимальная ставка теперь {new_max_stavka}', reply_markup=admin_keyboard)
        except:
            bot.send_message(us_id,f'Введите число!', reply_markup=admin_keyboard)

#Установка антиминуса
def new_antiminus(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    new_antiminus = message.text
    if message.text == 'Админка':
        adminka_menu(message)
    else:
        try:
            new_antiminus = int(new_antiminus)
            cursor.execute("UPDATE settings SET antiminus = ('%s') WHERE bot = 1"%(new_antiminus,))
            conn.commit()
            bot.send_message(us_id,f'Антиминус теперь {new_antiminus}', reply_markup=admin_keyboard)
        except:
            bot.send_message(us_id,f'Введите число!', reply_markup=admin_keyboard)





            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")

            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")