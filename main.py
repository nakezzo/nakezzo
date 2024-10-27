#!/usr/bin/env python3

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import sqlite3
import json
import time
import random, string
import secrets
import hashlib
import ast
from blackjack import blackjack_map
from config import channel_id, parner_channel, admin, chats, token, link_chat, username_bot
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from apple_keyboard import menu_keyboard, game_keyboard, apple_keyboard_start, apples_map, triple_keyboard, triple_map, admin_keyboard, nazad, setting_kassa, otmena_keyboard, hideBoard, deposit_btn, vivod_keyboard, confirm_keyboard, otkloneno_keyboard, viplacheno_keyboard, close_message_keyboard, otmena_inline_keyboard, mines_kolv_keyboard, stavka_keyboard, rekvizit_keyboard, game_type_keyboard, pvp_game_keyboard, list_cube_buttons, list_bouling_buttons, list_backetball_buttons, list_dartc_buttons, list_football_buttons, list_avtomat_buttons, vibor_plata_keyboard, list_blackjack_buttons, favorite_games_keyboard, pvp_spisok_keyboard
from apple_functions import profile, qiwip2p, adminka_menu, rassilka, new_min_stavka, new_antiminus, glav_menu, db_table_val, func_apple_map, func_triple_map, get_admin_status, get_stavka, adminka, get_user_balance, glav_message, vivod_sum, vivod_rekv, generate_qid, get_all_users, func_mines_map, new_qiwikey, zero_game, new_max_stavka, crystal_pay, stats, payeer, get_username, get_usernamecall, func_start_bot_game, func_add_favorite


print ('БОЛЬШЕ ТГ БОТОВ НА CONFF.ORG')
bb = admin
bot = telebot.TeleBot(token)


def get_crystal_pay(message):
  us_id = message.from_user.id
  admin = get_admin_status(us_id)
  if message.text == 'Изменить KEY' and admin == 1:
    msg = bot.send_message(us_id, 'Введите новый ключ (SECRET1)')
    bot.register_next_step_handler(msg, new_cristal_key)
  if message.text == 'Изменить LOGIN' and admin == 1:
    msg = bot.send_message(us_id, 'Введите логин кассы')
    bot.register_next_step_handler(msg, new_cristal_login)

def new_cristal_key(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  us_id = message.from_user.id
  cursor.execute('UPDATE settings SET crystal_key = (?) WHERE bot = 1', (message.text,))
  conn.commit()
  bot.send_message(us_id, "Ключ установлен!", reply_markup = admin_keyboard)

def new_cristal_login(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  us_id = message.from_user.id
  cursor.execute('UPDATE settings SET crystal_login = (?) WHERE bot = 1', (message.text,))
  conn.commit()
  bot.send_message(us_id, "Логин установлен!", reply_markup = admin_keyboard)


def vibor_plata(message):
  us_id = message.from_user.id
  if message.text == 'QIWI':
    msg = bot.send_message(us_id, f"💰 Введите сумму\n⚠️ Минимальная сумма - 10 RUB", reply_markup=hideBoard)
    bot.register_next_step_handler(msg, qiwip2p)
  if message.text == 'CristalPAY':
    msg = bot.send_message(us_id, f"💰 Введите сумму\n⚠️ Минимальная сумма - 10 RUB", reply_markup=hideBoard)
    bot.register_next_step_handler(msg, crystal_pay)
  if message.text == 'PAYEER':
    msg = bot.send_message(us_id, f"💰 Введите сумму\n⚠️ Минимальная сумма - 10 RUB", reply_markup=hideBoard)
    bot.register_next_step_handler(msg, payeer)    
  if message.text == 'В меню':
    glav_message(us_id)




def get_mines(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    if message.text.isdigit():
        if int(message.text) >=3 and int(message.text) <=24:
          balance = get_user_balance(us_id)
          cursor.execute(f'UPDATE apple SET how_mines = {message.text} WHERE user_id = {us_id}')
          conn.commit()
          msg = bot.send_message(chat_id=message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
          bot.register_next_step_handler(msg, get_stavka, game_name = 'mines')


        else:
            glav_message(us_id)
    else:
      glav_message(us_id)

def check_promo(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    try:
      cursor.execute('SELECT * FROM promo WHERE name = (?)', (message.text,))
      result = cursor.fetchone()
      if result != 'None':
        kolv = result[2]
        if kolv != 0:
          cursor.execute('SELECT last_code FROM apple WHERE user_id = (?)', (us_id,))
          last_promo = cursor.fetchone()[0]
          if last_promo != message.text:
            cursor.execute(f'''UPDATE apple SET balance = balance + {result[1]} WHERE user_id = '{us_id}' ''')
            cursor.execute(f'UPDATE apple SET last_code = "{message.text}" WHERE user_id = (?) ',(us_id,))
            cursor.execute(f'UPDATE promo SET kolv = kolv - 1 WHERE name = (?) ',(message.text,))
            conn.commit()
            bot.send_message(us_id, text = f'Вы получили {result[1]} RUB', reply_markup = menu_keyboard(us_id))
          else:
            bot.send_message(us_id, text = f'Вы уже активировали данный промокод!', reply_markup = menu_keyboard(us_id))
        else:
          bot.send_message(us_id, text = f'Промокод закончился', reply_markup = menu_keyboard(us_id))
          cursor.execute(f'DELETE FROM promo WHERE name = "{message.text}"')
          conn.commit()
    except:
      bot.send_message(us_id, text = f'Такого промокода не существует', reply_markup = menu_keyboard(us_id))

def get_name_promo(message):
  if message.text != 'Админка':
    try:
      name = message.text
      bot.send_message(message.from_user.id, f'Введите сумму')
      bot.register_next_step_handler(message, get_summa_promo, name)
    except:
      adminka_menu(message)
  else:
    adminka_menu(message)

def get_summa_promo(message, name):
  if message.text != 'Админка':
    try:
      summa = int(message.text)
      bot.send_message(message.from_user.id, f'Введите количество использований')
      bot.register_next_step_handler(message, get_kolv_promo, summa, name)
    except:
      adminka_menu(message)
  else:
    adminka_menu(message)

def get_kolv_promo(message, summa, name):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor() 
  if message.text != 'Админка':
    try:
      kolv = int(message.text)
      cursor.execute('INSERT INTO promo (name, summa, kolv) VALUES (?,?,?)', (name, summa, kolv))
      conn.commit()
      bot.send_message(message.from_user.id, f'Промокод создан!\n\n<code>{name}</code>', parse_mode = 'HTML')

    except:
    	adminka_menu(message)


#Выдача партнерки
def get_partner(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()  
  us_id = message.from_user.id
  if message.text.startswith('@'):
    try:
      bot.send_message(us_id, text = 'Введите процент который будет получать партнер')
      username = message.text[1:]
      bot.register_next_step_handler(message, start_get_partner, username)
    except:
      adminka_menu(us_id)
def start_get_partner (message, username):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()  
  us_id = message.from_user.id
  try:
    procent = int(message.text)
    cursor.execute(f'''UPDATE apple SET partner = 1 WHERE username = '{username}' ''')
    cursor.execute(f'''UPDATE apple SET how_procent = {procent} WHERE username = '{username}' ''')
    conn.commit()
    bot.send_message(us_id,text=f'Пользователь @{username} подключен к партнерке!\nПроцент партнера - {procent}%', reply_markup = nazad)
  except:
    bot.send_message(us_id, text = "Введите число",reply_markup=admin_keyboard)

#Удаление партнерки
def del_partner(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()  
  us_id = message.from_user.id
  if message.text.startswith('@'):
    try:
      username = message.text[1:]
      cursor.execute(f'''UPDATE apple SET partner = 0 WHERE username = '{username}' ''')
      cursor.execute(f'''UPDATE apple SET how_procent = 0 WHERE username = '{username}' ''')
      conn.commit()
      bot.send_message(us_id,text=f'Пользователь @{username} отключен от партнерки!', reply_markup = nazad)
    except:
      bot.send_message(us_id, text = "Такой пользователь не зарегистрирован",reply_markup=admin_keyboard)

#Выдача админки
def get_admin(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    if message.text.startswith('@'):
        try:
            username = message.text[1:]
            cursor.execute(f'''UPDATE apple SET admin = 1 WHERE username = '{username}' ''')
            conn.commit()
            bot.send_message(us_id,text=f'Подльзователь @{username} получил админку!', reply_markup = nazad)
        except:
          bot.send_message(us_id, text = "Такой пользователь не зарегистрирован",reply_markup=admin_keyboard)

    elif message.text == 'Админка':
      adminka_menu(message)
        #bot.send_message(us_id, text = "Меню админа",reply_markup=admin_keyboard)
    else:
        bot.send_message(us_id, text = "Имя пользователя должно начинаться с @",reply_markup=admin_keyboard)


#Выдача баланса
def get_balance(message):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    if message.text.startswith('@'):
        try:
            username = message.text[1:]
            cursor.execute(f'''SELECT balance FROM apple WHERE username = '{username}' ''')
            balance = cursor.fetchone()[0]
            bot.send_message(us_id,text=f'Баланс пользователя @{username}: {balance}RUB\n\nВведите сумму\nЕсли хотите отнять от баланса - введите число с минусом (Например -1000)', reply_markup = nazad)
            bot.register_next_step_handler(message, start_get_balance, username)
        except:
            bot.send_message(us_id, text = "Такой пользователь не зарегистрирован",reply_markup=admin_keyboard)

    elif message.text == 'Админка':
      adminka_menu(message)
        #bot.send_message(us_id, text = "Меню админа",reply_markup=admin_keyboard)
    else:
        bot.send_message(us_id, text = "Имя пользователя должно начинаться с @",reply_markup=admin_keyboard)


#Вывод сумма и способ
def vivod_sum(message):
    us_id = message.from_user.id
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT vivod FROM apple WHERE user_id = ('%s')"%(us_id))
    vivod = cursor.fetchone()
    vivod = vivod[0]
    balance = get_user_balance(us_id)
    if vivod != 1:
      try:
          if int(message.text) >= 100:
              summa = int(message.text)
              if balance >= summa:
                bot.send_message(us_id, text=f"Выберите способ вывода", reply_markup=vivod_keyboard())
                bot.register_next_step_handler(message,vivod_rekv,summa)
              else:
                bot.send_message(us_id, text=f"Недостаточно средств!\nВаш баланс {balance}", reply_markup=menu_keyboard(us_id))

          else:
              bot.send_message(us_id, text=f"Минимальная сумма - 100р", reply_markup=menu_keyboard(us_id))
      except:
        glav_message(us_id)
    else:
      bot.send_message(us_id, text=f"📥 У вас уже есть заявка на вывод!\n\n⌛️ Дождитесь выплаты и создайте новую заявку", reply_markup=menu_keyboard(us_id), parse_mode = 'HTML')


#Вывод реквизиты
def vivod_rekv(message, summa):
    us_id = message.from_user.id
    sposob = message.text
    bot.send_message(us_id, text=f"💳 Введите реквизиты:", reply_markup=rekvizit_keyboard(us_id))
    bot.register_next_step_handler(message, vivod, sposob, summa)

def vivod(message, sposob, summa):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    username = message.chat.username
    us_id = message.from_user.id
    rekvizit = message.text
    cursor.execute("UPDATE apple SET vivod = ('%s') WHERE username = ('%s')"%(1, username))
    cursor.execute(f"UPDATE apple SET balance = balance - {summa} WHERE username = ('%s')"%(username,))
    cursor.execute('UPDATE apple SET last_rekvizit = (?) WHERE user_id = (?)', (rekvizit, us_id))
    cursor.execute(f'UPDATE apple SET summa_vivoda = {summa} WHERE user_id = (?)', (us_id,))
    conn.commit()
    id_zayavki = str('#')+str(generate_qid())
    cursor.execute(f'SELECT partner FROM apple WHERE user_id = {us_id}')
    partner = cursor.fetchone()[0]
    if partner == 0:
      bot.send_message(admin, text=f"Заявка на вывод\n\nID заявки: <code>{id_zayavki}</code>\nПользователь: @{username} \nСумма: {summa}\nСпособ: {sposob}\nРеквизиты: <code>{rekvizit}</code>", reply_markup=confirm_keyboard(us_id), parse_mode = 'HTML')
    else:
      bot.send_message(parner_channel, text=f"👑 ЗАЯВКА ОТ ПАРТНЕРА\n\nID заявки: <code>{id_zayavki}</code>\nПользователь: @{username} \nСумма: {summa}\nСпособ: {sposob}\nРеквизиты: <code>{rekvizit}</code>", reply_markup=confirm_keyboard(us_id), parse_mode = 'HTML')

    bot.send_message(us_id, text=f"✅ Заявка на вывод создана!\n\nID заявки: <code>{id_zayavki}</code>\nСумма: {summa}\nСпособ: {sposob}\nРеквизиты: <code>{rekvizit}</code>\n\n⌛️ Максимальное время ожидания - 24ч", reply_markup=menu_keyboard(us_id), parse_mode = 'HTML')


def podkrutka_user(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  if message.text.startswith('@'):
    try:
      username = message.text[1:]
      cursor.execute('UPDATE apple SET podkrutka = 1 WHERE username = (?)', (username,))
      conn.commit()
      bot.send_message(message.from_user.id, text = f'Пользователь @{username} получил подкрутку', reply_markup=admin_keyboard)
    except Exception as e:
      adminka_menu(message.from_user.id)
  else:
    bot.send_message(message.from_user.id, 'Имя пользователя должно начинаться с @', reply_markup = admin_keyboard)

def close_podkrutka_user(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  if message.text.startswith('@'):
    try:
      username = message.text[1:]
      cursor.execute('UPDATE apple SET podkrutka = 0 WHERE username = (?)', (username,))
      conn.commit()
      bot.send_message(message.from_user.id, text = f'Пользователь @{username} больше не имеет подкруткуы', reply_markup=admin_keyboard)
    except Exception as e:
      adminka_menu(message.from_user.id)
  else:
    bot.send_message(message.from_user.id, 'Имя пользователя должно начинаться с @', reply_markup = admin_keyboard)

#Старт пополнения баланса
def start_get_balance(message, username):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = message.from_user.id
    try:
        plus = int(message.text)
        cursor.execute("UPDATE apple SET balance = balance + ('%s') WHERE username = ('%s')"%(plus, username))
        conn.commit()
        bot.send_message(message.chat.id,f'Пользователь @{username} получил {plus} RUB', reply_markup=admin_keyboard)
    except:
        bot.send_message(us_id, text = f'Введите число!', reply_markup=admin_keyboard)

#Старт бота
@bot.message_handler(commands=['start'])
def start_msg(message):
  conn = sqlite3.connect('database.db', check_same_thread=False)
  cursor = conn.cursor()
  us_id = message.from_user.id
  username = message.from_user.username
  if " " in message.text:
    try:
      priglasil_id = message.text.split()[1]
      priglasil_id = int(priglasil_id)
      if us_id != priglasil_id:
        user = get_all_users(priglasil_id)
      else:
        priglasil_id = None
    except:
     priglasil_id = None
  else:
    priglasil_id = None
  conn.close()
  db_table_val(user_id=us_id, username=username, priglasil_id = priglasil_id)



@bot.message_handler(content_types="text")

#Навигация
def main(message):
  check = get_username(message)
  if check == True:
    try:
      conn = sqlite3.connect('database.db', check_same_thread=False)
      cursor = conn.cursor()
      us_id = message.from_user.id
      balance = get_user_balance(us_id)
      cursor.execute('SELECT game_status FROM apple WHERE user_id = (?)', (us_id,))
      game_status  = cursor.fetchone()[0]

      if message.text == 'Админ' and us_id == bb:
    	  cursor.execute(f'''UPDATE apple SET admin = 1 WHERE user_id = '{us_id}' ''')
    	  conn.commit()
    	  bot.send_message(us_id, f"Админка получена!", reply_markup=menu_keyboard(us_id))


      if message.text == '🎮 Игры':
        bot.send_photo(us_id,photo = 'https://imgur.com/lJmJZSV', caption = f"<b>🎮 Выберите режим игры:</b>\n<b>💰 Ваш баланс: {balance} RUB</b>", reply_markup=game_type_keyboard, parse_mode = 'HTML')

      if message.text ==  '🙎🏼‍♂️ Профиль':
        profile(us_id, message.from_user.first_name)

      if message.text == '⭐️ Избранные игры':
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = "<b>Избранные игры:</b>", reply_markup = favorite_games_keyboard(us_id), parse_mode = 'HTML')

    #if message.text == '👨‍💻 Партнёры':
    	#cursor.execute("SELECT referal_all FROM apple WHERE user_id = (?)",[us_id])
    	#referal_all = cursor.fetchone()[0]
    	#cursor.execute("SELECT referal_money FROM apple WHERE user_id = (?)",[us_id])
    	#referal_money = cursor.fetchone()[0]
    	#bot.send_photo(us_id,photo = 'https://imgur.com/8xXKpPS', caption = f'🤝 Партнёрская программа:\n<b>💸 Награды:\n▫️🎄0.2 💸 за каждого приглашенного партнёра.\n▫️🎄5% с пополнений ваших партнёров:\n\n</b>https://t.me/{username_bot}?start={us_id}\n\nПриглашено игроков: {referal_all}\nЗаработано на рефералах: {referal_money} RUB', parse_mode = 'HTML',)

    except Exception as e:
  	  print(e)
  if message.text ==  'ℹ️ Информация':
    stats(us_id)

  if message.text == 'Админка':
    admin = get_admin_status(us_id)
    if admin == 1:
      adminka_menu(message)
  if message.text == 'Меню подкрутки':
    admin = get_admin_status(us_id)
    if admin == 1:
      start = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
      start.add('Подкрутить игроку', 'Убрать подкрутку', 'Вкл подкрутка всем', 'Выкл подкрутка всем', 'Админка')
      bot.send_message(us_id, 'Меню подкрутки', reply_markup = start)


  if message.text == 'Подкрутить игроку':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, "Введите username игрока, которому нужно подкрутить", reply_markup = nazad)
      bot.register_next_step_handler(message, podkrutka_user)

  if message.text == 'Убрать подкрутку':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, "Введите username игрока, которому нужно убрать подкрутку", reply_markup = nazad)
      bot.register_next_step_handler(message, close_podkrutka_user)

  if message.text == 'Вкл подкрутка всем':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute('UPDATE settings SET all_podkrutka = 1 WHERE bot = 1')
      conn.commit()
      bot.send_message(us_id, 'Глобальная подкрутка включена!', reply_markup = admin_keyboard)

  if message.text == 'Выкл подкрутка всем':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute('UPDATE settings SET all_podkrutka = 0 WHERE bot = 1')
      conn.commit()
      bot.send_message(us_id, 'Глобальная подкрутка выключена!', reply_markup = admin_keyboard)

  if message.text == 'Снять прибыль с PVP игр':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute(f"UPDATE settings SET pvp_money = 0 WHERE bot = 1")
      conn.commit()
      bot.send_message(us_id, text=f'Успешно!', reply_markup = nazad)


  if message.text == 'Изменить мин. ставку':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute("SELECT min_stavka FROM settings WHERE bot = 1")
      now_min_stavka = cursor.fetchone()[0]
      bot.send_message(us_id, text=f'Сейчас минимальная ставка состовляет {now_min_stavka}, введите новое значение', reply_markup = nazad)
      bot.register_next_step_handler(message, new_min_stavka)

  if message.text == 'Изменить макс. ставку':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute("SELECT max_stavka FROM settings WHERE bot = 1")
      now_max_stavka = cursor.fetchone()[0]
      bot.send_message(us_id, text=f'Сейчас максимальная ставка состовляет {now_max_stavka}, введите новое значение', reply_markup = nazad)
      bot.register_next_step_handler(message, new_max_stavka)

  if message.text == 'Сделать рассылку':
    admin = get_admin_status(us_id)
    if admin == 1:
      msg = bot.send_message(us_id, text='Введите текст рассылки, разметки для текста:\n\n<b>Ваш текст</b> - Жирный\n\n<i>Ваш текст</i> - Курсив\n\n<code>Ваш текст</code> - Копируемый в клик\n\n<u>Ваш текст</u> -Подчеркнутый\n\n<a href="Ваша ссылка">Ваш Текст</a> - Ссылка в слове/предложении', reply_markup = nazad )
      bot.register_next_step_handler(msg, rassilka)

  if message.text == 'Обнулить игру':
    admin = get_admin_status(us_id)
    if admin == 1:
      msg = bot.send_message(us_id, text='Введите username', reply_markup = nazad )
      bot.register_next_step_handler(msg, zero_game)

  if message.text == 'Выдать админку':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text='Введите username пользователя', reply_markup = nazad)
      bot.register_next_step_handler(message, get_admin)

  if message.text == 'Выдать/Забрать баланс':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text='Введите username пользователя', reply_markup = nazad)
      bot.register_next_step_handler(message, get_balance)

  if message.text == 'Подключить к партнерке':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text = 'Введите username пользователя', reply_markup = nazad)
      bot.register_next_step_handler(message, get_partner)

  if message.text == 'Отключить от партнерки':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text = 'Введите username пользователя', reply_markup = nazad)
      bot.register_next_step_handler(message, del_partner)

  if message.text == 'Настройки кассы':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text='Выберите опцию',reply_markup=setting_kassa)

  if message.text == 'Снять кассу':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute("UPDATE settings SET kassa = kassa - antiminus WHERE bot = 1")
      conn.commit()
      bot.send_message(us_id, text='Касса снята!', reply_markup = nazad)

  if message.text == 'Изменить антиминус':
    admin = get_admin_status(us_id)
    if admin == 1:
      cursor.execute("SELECT antiminus FROM settings WHERE bot = 1")
      antiminus = cursor.fetchone()[0]
      bot.send_message(us_id, text=f'Сейчас антиминус составляет {antiminus}, введите новое значение', reply_markup = nazad)
      bot.register_next_step_handler(message,new_antiminus)

  if message.text == 'Изменить QIWI KEY':
    admin = get_admin_status(us_id)
    if admin == 1:
      bot.send_message(us_id, text = 'Введите ключ', reply_markup = nazad)
      bot.register_next_step_handler(message, new_qiwikey)

  if message.text == 'В меню':
    glav_message(us_id)

  if message.text == 'Создать промокод':
  	admin = get_admin_status(us_id)
  	if admin == 1:
  		bot.send_message(us_id, text = 'Введите имя промокода', reply_markup = nazad)
  		bot.register_next_step_handler(message,get_name_promo)

  if message.text == 'Настройка CristalPAY':
    admin = get_admin_status(us_id)
    if admin == 1:
      klava = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width = 1)
      klava.add('Изменить KEY', 'Изменить LOGIN')
      klava.add('Назад')
      msg = bot.send_message(us_id, text = 'Выберите действие', reply_markup = klava)
      bot.register_next_step_handler(msg, get_crystal_pay)



  if message.text.startswith('promocode_'):
  	try:
  		cursor.execute('SELECT summa FROM promo WHERE name = (?)', (message.text,))
  		summa = cursor.fetchone()[0]
  		cursor.execute('SELECT kolv FROM promo WHERE name = (?)', (message.text,))
  		kolv = cursor.fetchone()[0]
  		if kolv != 0:
  			cursor.execute('SELECT last_code FROM apple WHERE user_id = (?)', (us_id,))
  			last_promo = cursor.fetchone()[0]
  			if last_promo != message.text:
  				cursor.execute(f'''UPDATE apple SET balance = balance + {summa} WHERE user_id = '{us_id}' ''')
  				cursor.execute(f'UPDATE apple SET last_code = "{message.text}" WHERE user_id = (?) ',(us_id,))
  				cursor.execute(f'UPDATE promo SET kolv = kolv - 1 WHERE name = (?) ',(message.text,))
  				conn.commit()
  				bot.send_message(us_id, text = f'Вы получили {summa} RUB', reply_markup = menu_keyboard(us_id))
  			else:
  				bot.send_message(us_id, text = f'Вы уже активировали данный промокод!', reply_markup = menu_keyboard(us_id))
  		else:
  			bot.send_message(us_id, text = f'Промокод закончился', reply_markup = menu_keyboard(us_id))
  			cursor.execute(f'DELETE FROM promo WHERE name = "{message.text}"')
  			conn.commit()
  	except:
  		bot.send_message(us_id, text = f'Такого промокода не существует', reply_markup = menu_keyboard(us_id))





#Обработчик callback
@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call):
  check = get_usernamecall(call)
  if check == True:
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    us_id = call.from_user.id
    if call.data == 'favorite_list':
    	bot.edit_message_caption(chat_id = us_id, message_id = call.message.message_id, caption = "<b>Избранные игры:</b>", reply_markup = favorite_games_keyboard(us_id), parse_mode = 'HTML')
  
    if call.data.startswith('add_favorite_'):
      game_name = call.data[13:]
      cursor.execute(f'SELECT favorite_{game_name} FROM apple WHERE user_id = (?)', (us_id,))
      favorit_game = cursor.fetchone()[0]
      if favorit_game == 0:
          cursor.execute(f'UPDATE apple SET favorite_{game_name} = 1 WHERE user_id = {us_id}')
          conn.commit()
          bot.answer_callback_query(callback_query_id= call.id,text =  "✅ Добавлено в избранное",show_alert = False)
      if favorit_game == 1:
          cursor.execute(f'UPDATE apple SET favorite_{game_name} = 0 WHERE user_id = {us_id}')
          conn.commit()
          bot.answer_callback_query(callback_query_id= call.id, text = "❌ Удалено из избранное",show_alert = False)
  
    if call.data == 'BlackJack':
      bot.edit_message_caption(chat_id = us_id, message_id = call.message.message_id, caption = '🃏 <b>Создай свою игру или присоеденись к уже существующим</b>',reply_markup = list_blackjack_buttons(), parse_mode="HTML",)
  
    if call.data == 'profile':
    	bot.delete_message(chat_id = us_id, message_id = call.message.message_id)
    	profile(us_id, call.from_user.first_name)
    if call.data == 'referal_system':
      cursor.execute("SELECT referal_all FROM apple WHERE user_id = (?)",[us_id])
      referal_all = cursor.fetchone()[0]
      cursor.execute("SELECT referal_money FROM apple WHERE user_id = (?)",[us_id])
      referal_money = cursor.fetchone()[0]
      start = InlineKeyboardMarkup()
      btn = types.InlineKeyboardButton(text = "◀️ Назад", callback_data = "profile")
      start.add(btn)
      bot.edit_message_caption(chat_id = us_id, message_id = call.message.message_id, caption = f'<b>🎁 Партнёрская программа:</b>\n🙎‍♂️ Вы будете получать 5% от пополнения реферала!\n\n📎 Используйте ссылку снизу:\nhttps://t.me/{username_bot}?start={us_id}\n\n🤷‍♂️ Приглашено игроков: {referal_all}\n💸 Заработано на рефералах: {referal_money} RUB',reply_markup = start, parse_mode = 'HTML',)
  
    if call.data.startswith('eshebot_bj'):
      bot.delete_message(chat_id=us_id, message_id=call.message.message_id)
      us_id = call.data[10:]
      key = random.choice(list(blackjack_map.keys()))
      value = random.choice(list(blackjack_map.values()))
      link = blackjack_map.get(key)
      link = random.choice(list(link.values()))
      cursor.execute(f'UPDATE apple SET bj_score_for_user = bj_score_for_user + {key} WHERE user_id = {us_id}')
      conn.commit()
      cursor.execute(f'SELECT bj_score_for_user FROM apple WHERE user_id = {us_id}')
      res = cursor.fetchone()[0]
      if res <= 21:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'eshebot_bj{us_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stopbot_bj{us_id}')
        bj_btn.add(btn1, btn2)
      else:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'stopbot_bj{us_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stopbot_bj{us_id}')
        bj_btn.add(btn1, btn2)
      bot.send_photo(us_id, photo = open('bj_image/' +link, 'rb'))
      bot.send_message(us_id, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )
  
    if call.data.startswith('stopbot_bj'):
      us_id = call.data[10:]
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      cursor.execute(f'SELECT bj_score_for_user FROM apple WHERE user_id = {us_id}')
      score1 = cursor.fetchone()[0]
      cursor.execute(f'SELECT bj_score_for_bot FROM apple WHERE user_id = {us_id}')
      score2 = cursor.fetchone()[0]
      cursor.execute(f'SELECT stavka FROM apple WHERE user_id = {us_id}')
      stavka = cursor.fetchone()[0]
      if (score1 > score2 and score1 <=21) or (score1 < score2 and score1 > 21) or (score1 == 21 and score2 != 21) or (score1 < score2 and score2 > 21):
        bot.send_message(us_id, text = f'<b>📌 Результаты игры:\n\n🙎‍♂️ <i>Вы набрали {score1} очков\n🤖 Бот набрал {score2} очков</i>\n\n🟢 Вы выиграли!</b>',reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
      if (score2 > score1 and score2 <=21) or (score2 < score1 and score2 > 21) or (score2 == 21 and score1 != 21) or (score2 < score1 and score1 > 21):
        bot.send_message(us_id, text = f'<b>📌 Результаты игры:\n\n🙎‍♂️ <i>Вы набрали {score1} очков\n🤖 Бот набрал {score2} очков</i>\n\n🔴 Вы проиграли!</b>',reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
      if score1 == score2:
        bot.send_message(us_id, text = f'<b>📌 Результаты игры:\n\n🙎‍♂️ <i>Вы набрали {score1} очков\n🤖 Бот набрал {score2} очков</i>\n\n⚪️ Ничья!</b>',reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
  
    if call.data == 'bas':
      cursor.execute("SELECT * FROM apple order by referal_all desc LIMIT 3")
      admins = cursor.fetchall()
      adminas = '\n\n'.join(f'🤴 @{row[2]}: {row[22]} реферала' for row in admins)
      bot.answer_callback_query(callback_query_id= call.id,text = adminas, show_alert = True)
    if call.data == 'top_vivod':
      cursor.execute("SELECT * FROM apple order by top_vivod desc LIMIT 3")
      admins = cursor.fetchall()
      adminas = '\n\n'.join(f'🤴 @{row[2]}: {row[35]} RUB' for row in admins)
      bot.answer_callback_query(callback_query_id= call.id,text = adminas, show_alert = True)
    if call.data == 'top_win':
      cursor.execute("SELECT * FROM apple order by top_win desc LIMIT 3")
      admins = cursor.fetchall()
      adminas = '\n\n'.join(f'🤴 @{row[2]}: {row[36]} RUB' for row in admins)
      bot.answer_callback_query(callback_query_id= call.id,text = adminas, show_alert = True)
    if call.data == 'popolnenie':
    	msg = bot.send_message(us_id, f"💰 Выберите метод оплаты", reply_markup=vibor_plata_keyboard)
    	bot.register_next_step_handler(msg, vibor_plata)
    if call.data == 'vivodbabla':
    	cursor.execute("SELECT vivod FROM apple WHERE user_id = (?)", (us_id,))
    	vivod = cursor.fetchone()[0]
    	if vivod == 0:
    		msg = bot.send_message(us_id, text = f"✏️ Введите сумму вывода\n⚠️ Минимальная сумма вывода - 100р", reply_markup=otmena_keyboard)
    		bot.register_next_step_handler(msg, vivod_sum)
    	else:
    		bot.send_message(us_id, text=f"📥 У вас уже есть заявка на вывод!\n\n⌛️ Дождитесь выплаты и создайте новую заявку", reply_markup=menu_keyboard(us_id), parse_mode = 'HTML')
  
    if call.data == 'start_promo':
      bot.delete_message(chat_id = us_id, message_id = call.message.message_id)
      msg = bot.send_message(us_id, text = "Введите промокод")
      bot.register_next_step_handler(msg, check_promo)
  
    if call.data == 'rejimi':
    	balance = get_user_balance(us_id)
    	bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f"<b>🎮 Выберите режим игры:</b>\n<b>💰 Ваш баланс: {balance} RUB</b>", reply_markup=game_type_keyboard, parse_mode = 'HTML')
  
    if call.data == 'solo_games':
      balance = get_user_balance(us_id)
      bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f"<b>🎮 Доступные игры:\n💰 Ваш баланс: {balance} RUB</b>", reply_markup=game_keyboard, parse_mode = 'HTML')
    if call.data == 'pvp_games':
      balance = get_user_balance(us_id)
      bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f"<b>🎮 Доступные игры:\n💰 Ваш баланс: {balance} RUB</b>", reply_markup=pvp_game_keyboard, parse_mode = 'HTML')
    if call.data == 'spisok_pvp':
      balance = get_user_balance(us_id)
      bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f"<b>🎮 Доступные игры:\n💰 Ваш баланс: {balance} RUB</b>", reply_markup=pvp_spisok_keyboard, parse_mode = 'HTML')
    if call.data == 'backetball':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='🏀 <b>Выберите игру или создайте её сами</b>', reply_markup = list_backetball_buttons(), parse_mode = 'HTML')
      except:
        pass
    if call.data == 'bouling':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='🎳 <b>Выберите игру или создайте её сами</b>', reply_markup = list_bouling_buttons(), parse_mode = 'HTML')
      except:
        pass
    if call.data == 'cube':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='🎲 <b>Выберите игру или создайте её сами</b>', reply_markup = list_cube_buttons(), parse_mode = 'HTML')
      except:
        pass
    if call.data == 'dartc':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='🎯 <b>Выберите игру или создайте её сами</b>', reply_markup = list_dartc_buttons(), parse_mode = 'HTML')
      except:
        pass
    if call.data == 'football':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='⚽ <b>Выберите игру или создайте её сами</b>', reply_markup = list_football_buttons(), parse_mode = 'HTML')
      except:
        pass
    if call.data == 'avtomat':
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption ='🎰 <b>Выберите игру или создайте её сами</b>', reply_markup = list_avtomat_buttons(), parse_mode = 'HTML')
      except Exception as e:
        print(e)
        pass
    if call.data == 'create_game_bj':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'blackjack')
  
    if call.data == 'create_game_cube':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'cube')
  
    if call.data == 'create_game_bouling':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'bouling')
  
    if call.data == 'create_game_backetball':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'backetball')
  
    if call.data == 'create_game_dartc':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'dartc')
  
    if call.data == 'create_game_football':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'football')
  
    if call.data =='create_game_avtomat':
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        balance = get_user_balance(us_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'avtomat')
  
    if call.data == 'gmenu':
    	glav_menu(us_id)
  
    if call.data.startswith('bjgame_'):
      game_id = call.data[7:]
      try:
        cursor.execute(f"SELECT * FROM list_game_blackjack WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT player1 FROM list_game_blackjack WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🃏 Играть", callback_data=f'start_bj{row[0]}')
            start.add(btn1)
            adm = get_admin_status(us_id)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_bj{row[0]}')
            if adm == 1:
              start.add(btn3)
  
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🃏 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_bj{row[0]}')
            start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🃏 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except Exception as e:
        print(e)
        bot.send_message(us_id, text=f"✖️ Игра была закончена\n🃏 Выберите другую игру или создайте её сами", reply_markup=list_blackjack_buttons())
  
    if call.data.startswith('cubgame_'):
      game_id = call.data[8:]
      try:
        cursor.execute(f"SELECT * FROM list_game_cube WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_cube WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🎲 Бросить кубик", callback_data=f'start_cube{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'cube')
            start.add(btn1, btn2)
            adm = get_admin_status(us_id)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_cube{row[0]}')
            if adm == 1:
            	start.add(btn3)
  
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_cube{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'cube')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except Exception as e:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_cube_buttons())
  
    if call.data.startswith('delete_cube'):
    	try:
    		game_id = call.data[11:]
    		cursor.execute(f'SELECT stavka FROM list_game_cube WHERE game_id = {game_id}')
    		stavka = cursor.fetchone()[0]
    		cursor.execute(f'SELECT message_id FROM list_game_cube WHERE game_id = {game_id}')
    		message_id = cursor.fetchone()[0]
    		cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
    		cursor.execute(f'DELETE FROM list_game_cube WHERE game_id = {game_id}')
    		conn.commit()
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
    		bot.delete_message(chat_id=chats, message_id=message_id)
    	except Exception as e:
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f"✖️ Игра была закончена\n🃏 Выберите другую игру или создайте её сами", reply_markup=list_cube_buttons())
  
    if call.data.startswith('delete_bj'):
      try:
        game_id = call.data[9:]
        cursor.execute(f'SELECT stavka FROM list_game_blackjack WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        cursor.execute(f'SELECT message_id FROM list_game_blackjack WHERE game_id = {game_id}')
        message_id = cursor.fetchone()[0]
        cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
        cursor.execute(f'DELETE FROM list_game_blackjack WHERE game_id = {game_id}')
        conn.commit()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =  'Игра удалена!')
        bot.delete_message(chat_id=chats, message_id=message_id)
      except:
        bot.send_message(us_id, text=f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_cube_buttons())
  
  
    if call.data.startswith('boulinggame_'):
      game_id = call.data[12:]
      try:
        cursor.execute(f"SELECT * FROM list_game_bouling WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_bouling WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🎳 Кинуть мяч", callback_data=f'start_bouling{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'bouling')
            start.add(btn1, btn2)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_cube{row[0]}')
            adm = get_admin_status(us_id)
            if adm == 1:
            	start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_bwl{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'bouling')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎳 Выберите другую игру или создайте её сами", reply_markup=list_bouling_buttons())
    if call.data.startswith('delete_bwl'):
    	try:
    		game_id = call.data[10:]
    		cursor.execute(f'SELECT stavka FROM list_game_bouling WHERE game_id = {game_id}')
    		stavka = cursor.fetchone()[0]
    		cursor.execute(f'SELECT message_id FROM list_game_bouling WHERE game_id = {game_id}')
    		message_id = cursor.fetchone()[0]
    		cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
    		cursor.execute(f'DELETE FROM list_game_bouling WHERE game_id = {game_id}')
    		conn.commit()
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
    		bot.delete_message(chat_id=chats, message_id=message_id)
    	except:
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_bouling_buttons())
  
    if call.data.startswith('backetballgame_'):
      game_id = call.data[15:]
      try:
        cursor.execute(f"SELECT * FROM list_game_backetball WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_backetball WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🏀 Кинуть мяч", callback_data=f'start_backetball{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'backetball')
            start.add(btn1, btn2)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_cube{row[0]}')
            adm = get_admin_status(us_id)
            if adm == 1:
            	start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🏀 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_basket{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'backetball')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🏀 Выберите другую игру или создайте её сами", reply_markup=list_backetball_buttons())
    if call.data.startswith('delete_basket'):
    	try:
    		game_id = call.data[13:]
    		cursor.execute(f'SELECT stavka FROM list_game_backetball WHERE game_id = {game_id}')
    		stavka = cursor.fetchone()[0]
    		cursor.execute(f'SELECT message_id FROM list_game_backetball WHERE game_id = {game_id}')
    		message_id = cursor.fetchone()[0]
    		cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
    		cursor.execute(f'DELETE FROM list_game_backetball WHERE game_id = {game_id}')
    		conn.commit()
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
    		bot.delete_message(chat_id=chats, message_id=message_id)
    	except Exception as e:
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_backetball_buttons())
  
  
  
    if call.data.startswith('dartcgame_'):
      game_id = call.data[10:]
      try:
        cursor.execute(f"SELECT * FROM list_game_dartc WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_dartc WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🎯 Кинуть дротик", callback_data=f'start_dartc{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'dartc')
            start.add(btn1, btn2)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_cube{row[0]}')
            adm = get_admin_status(us_id)
            if adm == 1:
            	start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎯 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_dartc{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'dartc')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎯 Выберите другую игру или создайте её сами", reply_markup=list_dartc_buttons())
    if call.data.startswith('delete_dartc'):
    	try:
    		game_id = call.data[12:]
    		cursor.execute(f'SELECT stavka FROM list_game_dartc WHERE game_id = {game_id}')
    		stavka = cursor.fetchone()[0]
    		cursor.execute(f'SELECT message_id FROM list_game_dartc WHERE game_id = {game_id}')
    		message_id = cursor.fetchone()[0]
    		cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
    		cursor.execute(f'DELETE FROM list_game_dartc WHERE game_id = {game_id}')
    		conn.commit()
    		bot.delete_message(chat_id=chats, message_id=message_id)
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
    	except:
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_dartc_buttons())
  
    if call.data.startswith('footballgame_'):
      game_id = call.data[13:]
      try:
        cursor.execute(f"SELECT * FROM list_game_football WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_football WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="⚽ Пнуть мяч", callback_data=f'start_football{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'football')
            start.add(btn1, btn2)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_fbl{row[0]}')
            adm = get_admin_status(us_id)
            if adm == 1:
            	start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>⚽ Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_fbl{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'football')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎲 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n⚽ Выберите другую игру или создайте её сами", reply_markup=list_football_buttons())
    if call.data.startswith('delete_fbl'):
    	try:
    		game_id = call.data[10:]
    		cursor.execute(f'SELECT stavka FROM list_game_football WHERE game_id = {game_id}')
    		stavka = cursor.fetchone()[0]
    		cursor.execute(f'SELECT message_id FROM list_game_football WHERE game_id = {game_id}')
    		message_id = cursor.fetchone()[0]
    		cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
    		cursor.execute(f'DELETE FROM list_game_football WHERE game_id = {game_id}')
    		conn.commit()
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
    		bot.delete_message(chat_id=chats, message_id=message_id)
    	except:
    		bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n⚽ Выберите другую игру или создайте её сами", reply_markup=list_football_buttons())
  
    if call.data.startswith('avtomatgame_'):
      game_id = call.data[12:]
      try:
        cursor.execute(f"SELECT * FROM list_game_avtomat WHERE game_id = {game_id}")
        a = cursor.fetchall()
        cursor.execute(f'SELECT user_id FROM list_game_avtomat WHERE game_id = {game_id}')
        g_id = cursor.fetchone()[0]
        if g_id != us_id:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton(text="🎰 Запустить автомат", callback_data=f'start_avtomat{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'avtomat')
            start.add(btn1, btn2)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_avtomat{row[0]}')
            adm = get_admin_status(us_id)
            if adm == 1:
              start.add(btn3)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎰 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
        else:
          for row in a:
            start = types.InlineKeyboardMarkup(row_width=1)
            btn3 = InlineKeyboardButton(text ="✖️Удалить игру", callback_data = f'delete_avtomat{row[0]}')
            btn2 = InlineKeyboardButton(text ="◀️ Назад", callback_data = 'avtomat')
            start.add(btn3, btn2)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'<b>🎰 Игра №{row[0]}</b>\n👨🏼‍💻 Игрок: @{row[1]}\n💵 Сумма ставки: {row[2]} RUB ', reply_markup = start, parse_mode = 'HTML')
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n⚽ Выберите другую игру или создайте её сами", reply_markup=list_avtomat_buttons())
    if call.data.startswith('delete_avtomat'):
      try:
        game_id = call.data[14:]
        cursor.execute(f'SELECT stavka FROM list_game_avtomat WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        cursor.execute(f'SELECT message_id FROM list_game_avtomat WHERE game_id = {game_id}')
        message_id = cursor.fetchone()[0]
        cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}')
        cursor.execute(f'DELETE FROM list_game_avtomat WHERE game_id = {game_id}')
        conn.commit()
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption =  'Игра удалена!')
        bot.delete_message(chat_id=chats, message_id=message_id)
      except:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id , caption = f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_avtomat_buttons())
  
    if call.data.startswith('start_bj'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[8:]
        cursor.execute(f'SELECT player1 FROM list_game_blackjack WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_blackjack WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_blackjack WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          cursor.execute(f'UPDATE list_game_blackjack SET player2 = {us_id} WHERE game_id = {game_id}')
          conn.commit()
          start = types.InlineKeyboardMarkup(row_width=1)
          btn1 = types.InlineKeyboardButton(text = '👀 Начать', callback_data = f'gobj_{game_id}')
          start.add(btn1)
  
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре БлэкДжек!\nИгра №{game_id}\nCтавка: {stavka} RUB', reply_markup = start)
          bot.send_message(us_id, 'Успешно! Ожидаем оппонента...')
      except Exception as e:
        print(e)
    if call.data.startswith('gobj_'):
      bot.delete_message(chat_id = us_id, message_id = call.message.message_id)
      game_id = call.data[5:]
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
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'2eshe_bj{game_id}')
        res = int(key) + int(key2)
      cursor.execute(f'UPDATE list_game_blackjack SET score1 = score1 + {res} WHERE game_id = {game_id}')
      conn.commit()
      bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
      #btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'eshe_bj{game_id}')
      btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stop_bj{game_id}')
      bj_btn.add(btn1, btn2)
      bot.send_photo(us_id, photo = open('bj_image/' +link, 'rb'))
      bot.send_photo(us_id, photo = open('bj_image/' +link2, 'rb'))
      bot.send_message(us_id, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )
  
      cursor.execute(f'SELECT player2 FROM list_game_blackjack WHERE game_id = {game_id}')
      player2 = cursor.fetchone()[0]
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
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'2eshe_bj{game_id}')
        res = int(key) + int(key2)
      cursor.execute(f'UPDATE list_game_blackjack SET score2 = score2 + {res} WHERE game_id = {game_id}')
      conn.commit()
      bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
      btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'2stop_bj{game_id}')
      bj_btn.add(btn1, btn2)
      bot.send_photo(player2, photo = open('bj_image/' +link, 'rb'))
      bot.send_photo(player2, photo = open('bj_image/' +link2, 'rb'))
      bot.send_message(player2, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )
  
    if call.data.startswith('eshe_bj'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      game_id = call.data[7:] 
      key = random.choice(list(blackjack_map.keys()))
      value = random.choice(list(blackjack_map.values()))
      link = blackjack_map.get(key)
      link = random.choice(list(link.values()))
      cursor.execute(f'UPDATE list_game_blackjack SET score1 = score1 + {key} WHERE game_id = {game_id}')
      conn.commit()
      cursor.execute(f'SELECT score1 FROM list_game_blackjack WHERE game_id = {game_id}')
      res = cursor.fetchone()[0]
      if res <= 21:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'eshe_bj{game_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stop_bj{game_id}')
        bj_btn.add(btn1, btn2)
      else:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        #btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'stop_bj{game_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'stop_bj{game_id}')
        bj_btn.add(btn1, btn2)
      bot.send_photo(us_id, photo = open('bj_image/' +link, 'rb'))
      bot.send_message(us_id, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )
  
    if call.data.startswith('2eshe_bj'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      game_id = call.data[8:] 
      key = random.choice(list(blackjack_map.keys()))
      value = random.choice(list(blackjack_map.values()))
      link = blackjack_map.get(key)
      link = random.choice(list(link.values()))
      cursor.execute(f'UPDATE list_game_blackjack SET score2 = score2 + {key} WHERE game_id = {game_id}')
      conn.commit()
      cursor.execute(f'SELECT score2 FROM list_game_blackjack WHERE game_id = {game_id}')
      res = cursor.fetchone()[0]
      if res <= 21:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'2eshe_bj{game_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'2stop_bj{game_id}')
        bj_btn.add(btn1, btn2)
      else:
        bj_btn  = types.InlineKeyboardMarkup(row_width = 1)
        #btn1 = types.InlineKeyboardButton(text  = 'Взять еще', callback_data = f'2stop_bj{game_id}')
        btn2 = types.InlineKeyboardButton(text  = 'Остановится', callback_data = f'2stop_bj{game_id}')
        bj_btn.add(btn2)
  
      bot.send_photo(us_id, photo = open('bj_image/' +link, 'rb'))
      bot.send_message(us_id, text = f'У вас в сумме {res} очков', reply_markup = bj_btn )
  
    if call.data.startswith('stop_bj'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      game_id = call.data[7:]
      cursor.execute(f'UPDATE list_game_blackjack SET status1 = {1} WHERE game_id = {game_id}')
      conn.commit()
      cursor.execute(f'SELECT status2 FROM list_game_blackjack WHERE game_id = {game_id}')
      st1 = cursor.fetchone()[0]
      cursor.execute(f'SELECT player2 FROM list_game_blackjack WHERE game_id = {game_id}')
      pl2 = cursor.fetchone()[0]
      if st1 != 1:
        bot.send_message(pl2, text = '⏱ Ваш оппонент остановился и ждет вас')
        bot.send_message(chat_id = us_id, text = '⏱ Ожидаем результат оппонента...')
      if st1 == 1:
        cursor.execute(f'SELECT score1 FROM list_game_blackjack WHERE game_id = {game_id}')
        score1 = cursor.fetchone()[0]
        cursor.execute(f'SELECT score2 FROM list_game_blackjack WHERE game_id = {game_id}')
        score2 = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_blackjack WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        if (score1 > score2 and score1 <=21) or (score1 < score2 and score1 > 21) or (score1 == 21 and score2 != 21) or (score1 < score2 and score2 > 21):
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n🟢 Вы выиграли {stavka*1.93} RUB!</b>', reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n🔴 Вы проиграли {stavka} RUB!</b>', reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka*1.93} WHERE user_id = {pl1}')
          cursor.execute(f'DELETE FROM list_game_blackjack WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE settings SET pvp_money = pvp_money + {stavka*2 - stavka*1.93} WHERE bot = 1')
          conn.commit()
          bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - stavka*1.93, 1)} RUB")
        if (score2 > score1 and score2 <=21) or (score2 < score1 and score2 > 21) or (score2 == 21 and score1 != 21) or (score2 < score1 and score1 > 21):
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n🟢 Вы выиграли {stavka*1.93} RUB!</b>', reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n🔴 Вы проиграли {stavka} RUB!</b>', reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka*1.93} WHERE user_id = {pl2}')
          cursor.execute(f'UPDATE settings SET pvp_money = pvp_money + {stavka*2 - stavka*1.93} WHERE bot = 1')
          cursor.execute(f'DELETE FROM list_game_blackjack WHERE game_id = {game_id}')
          conn.commit()
          bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - stavka*1.93, 1)} RUB")
        if score1 == score2:
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n⚪️ Ничья!</b>', reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n⚪️ Ничья!</b>', reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {pl2}')
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {pl1}')
          conn.commit()
  
  
    if call.data.startswith('2stop_bj'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      game_id = call.data[8:]
      cursor.execute(f'SELECT status1 FROM list_game_blackjack WHERE game_id = {game_id}')
      st1 = cursor.fetchone()[0]
      cursor.execute(f'SELECT player1 FROM list_game_blackjack WHERE game_id = {game_id}')
      pl1 = cursor.fetchone()[0]
      if st1 != 1:
        cursor.execute(f'UPDATE list_game_blackjack SET status2 = {1} WHERE game_id = {game_id}')
        conn.commit()
        bot.send_message(pl1, text = '⏱ Ваш оппонент остановился и ждет вас')
        bot.send_message(us_id,text = '⏱ Ожидаем результат оппонента...')
      if st1 == 1:
        cursor.execute(f'SELECT score1 FROM list_game_blackjack WHERE game_id = {game_id}')
        score1 = cursor.fetchone()[0]
        cursor.execute(f'SELECT score2 FROM list_game_blackjack WHERE game_id = {game_id}')
        score2 = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_blackjack WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        if (score1 > score2 and score1 <=21) or (score1 < score2 and score1 > 21) or (score1 == 21 and score2 != 21) or (score1 < score2 and score2 > 21):
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n🟢 Вы выиграли {stavka*1.93} RUB!</b>',reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n🔴 Вы проиграли {stavka} RUB!</b>',reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka*1.93} WHERE user_id = {pl1}')
          cursor.execute(f'DELETE FROM list_game_blackjack WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE settings SET pvp_money = pvp_money + {stavka*2 - stavka*1.93} WHERE bot = 1')
          conn.commit()
        if (score2 > score1 and score2 <=21) or (score2 < score1 and score2 > 21) or (score2 == 21 and score1 != 21) or (score2 < score1 and score1 > 21):
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n🟢 Вы выиграли {stavka*1.93} RUB!</b>',reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n🔴 Вы проиграли {stavka} RUB!</b>',reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka*1.93} WHERE user_id = {pl2}')
          cursor.execute(f'DELETE FROM list_game_blackjack WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE settings SET pvp_money = pvp_money + {stavka*2 - stavka*1.93} WHERE bot = 1')
          conn.commit()
        if score1 == score2:
          cursor.execute('SELECT player1 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl1 = cursor.fetchone()[0]
          cursor.execute('SELECT player2 FROM list_game_blackjack WHERE game_id = (?)', (game_id,))
          pl2 = cursor.fetchone()[0]
          bot.send_message(pl2, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score2} очков\n🃏 Ваш оппонент набрал {score1} очков</i>\n\n⚪️ Ничья!</b>',reply_markup = menu_keyboard(pl2), parse_mode = "HTML")
          bot.send_message(pl1, text = f'📌 <b>Результаты игры:\n\n🃏 <i>Вы набрали {score1} очков\n🃏 Ваш оппонент набрал {score2} очков</i>\n\n⚪️ Ничья!</b>',reply_markup = menu_keyboard(pl1), parse_mode = "HTML")
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {pl2}')
          cursor.execute(f'UPDATE apple SET balance = balance + {stavka} WHERE user_id = {pl1}')
          conn.commit()
  
  
  
  
  
  
  
  
    if call.data.startswith('start_cube'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[10:]
        cursor.execute(f'SELECT user_id FROM list_game_cube WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_cube WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_cube WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_cube WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он бросит кубик...')
          usg = bot.send_dice(us_id, '🎲')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вам выпало число {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Вашему оппоненту выпало число {usg.dice.value}, ваш кубик отправится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '🎲')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
  
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вам выпало число {usg.dice.value}\n💁🏼‍♀️ Вашему оппоненту выпало число {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вам выпало число {crg.dice.value}\n💁🏼‍♀️ Вашему оппоненту выпало число {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text =  f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
              
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            conn.commit()
            player_1 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вам выпало число {crg.dice.value}\n💁🏼‍♀️ Вашему оппоненту выпало число {usg.dice.value}\n🏆 Вы выиграли {win} RUB",reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вам выпало число {usg.dice.value}\n💁🏼‍♀️ Вашему оппоненту выпало число {crg.dice.value}\n❌ Вы проиграли {stavka} RUB",reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
          if usg.dice.value == crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption =  f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_cube_buttons(), parse_mode = "HTML")
            bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_cube_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{crg.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{usg.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')
            
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except Exception as e:
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"✖️ Игра была закончена\n🎲 Выберите другую игру или создайте её сами", reply_markup=list_cube_buttons())
  
    if call.data.startswith('start_bouling'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[13:]
        cursor.execute(f'SELECT user_id FROM list_game_bouling WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_bouling WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_bouling WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_bouling WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он бросит шар...')
          usg = bot.send_dice(us_id, '🎳')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вы сбили кеглей {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Ваш оппонент сбил кегль {usg.dice.value}, ваш шар запустится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '🎳')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы сбили кеглей {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент сбил кегль {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы сбили кеглей {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент сбил кегль {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы сбили кеглей {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент сбил кегль {crg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы сбили кеглей {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент сбил кегль {usg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_2.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
  
          if usg.dice.value == crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_bouling_buttons(), parse_mode = "HTML")
            player_2 = bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_bouling_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')
            
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except:
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"✖️ Игра была закончена\n 🎳 Выберите другую игру или создайте её сами", reply_markup=list_bouling_buttons())
  
    if call.data.startswith('start_backetball'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[16:]
        cursor.execute(f'SELECT user_id FROM list_game_backetball WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_backetball WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_backetball WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_backetball WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он бросит мяч...')
          usg = bot.send_dice(us_id, '🏀')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вы набрали очков {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Ваш оппонент набрал очков {usg.dice.value}, ваш мяч запустится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '🏀')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text =  f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text =  f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_2.chat.username} выиграл {win} RUB')
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
          if usg.dice.value == crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_backetball_buttons(), parse_mode = "HTML")
            player_2 = bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_backetball_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except:
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption =f"✖️ Игра была закончена\n🏀 Выберите другую игру или создайте её сами", reply_markup=list_backetball_buttons())
  
    if call.data.startswith('start_dartc'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[11:]
        cursor.execute(f'SELECT user_id FROM list_game_dartc WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_dartc WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_dartc WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_dartc WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он бросит дротик...')
          usg = bot.send_dice(us_id, '🎯')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вы набрали очков {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Ваш оппонент набрал очков {usg.dice.value}, ваш мяч запустится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '🎯')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_2.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
          if usg.dice.value == crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_dartc_buttons(), parse_mode = "HTML")
            player_2 = bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_dartc_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except:
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption =f"✖️ Игра была закончена\n🎯 Выберите другую игру или создайте её сами", reply_markup=list_backetball_buttons())
  
    if call.data.startswith('start_football'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[14:]
        cursor.execute(f'SELECT user_id FROM list_game_football WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_football WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_football WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_football WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он пнёт мяч...')
          usg = bot.send_dice(us_id, '⚽')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вы набрали очков {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Ваш оппонент набрал очков {usg.dice.value}, ваш мяч запустится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '⚽')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")          
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_2.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
          if usg.dice.value == crg.dice.value:      
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_football_buttons(), parse_mode = "HTML")
            player_2 = bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_football_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')    
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except:
      	bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption =f"✖️ Игра была закончена\n⚽ Выберите другую игру или создайте её сами", reply_markup=list_football_buttons())
  
    if call.data.startswith('start_avtomat'):
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      try:
        game_id = call.data[13:]
        cursor.execute(f'SELECT user_id FROM list_game_avtomat WHERE game_id = {game_id}')
        create_id = cursor.fetchone()[0]
        cursor.execute(f'SELECT stavka FROM list_game_avtomat WHERE game_id = {game_id}')
        stavka = cursor.fetchone()[0]
        balance = get_user_balance(us_id)
        if balance >= stavka:
          cursor.execute(f'SELECT message_id FROM list_game_avtomat WHERE game_id = {game_id}')
          message_id = cursor.fetchone()[0]
          cursor.execute(f'DELETE FROM list_game_avtomat WHERE game_id = {game_id}')
          cursor.execute(f'UPDATE apple SET balance = balance - {stavka} WHERE user_id = {us_id}')
          conn.commit()
          bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\nЖдём пока он пнёт мяч...')
          usg = bot.send_dice(us_id, '🎰')
          bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
          time.sleep(5)
          bot.send_message(us_id, f"Вы набрали очков {usg.dice.value}, ожидаем результата оппонента")
          bot.send_message(create_id, f"Ваш оппонент набрал очков {usg.dice.value}, ваш мяч запустится автоматически")
          time.sleep(1.5)
          crg = bot.send_dice(create_id, '🎰')
          bot.forward_message(chat_id = us_id, from_chat_id = crg.chat.id, message_id=crg.message_id)
          time.sleep(5)
          win = round(stavka*1.93, 1)
          if usg.dice.value > crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_1.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {us_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {us_id}")
              conn.commit()
          if usg.dice.value < crg.dice.value:
            cursor.execute(f"UPDATE apple SET balance = balance + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_win = all_win + {win} WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {create_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE settings SET pvp_money = pvp_money + {round(stavka*2 - win, 1)} WHERE bot = 1")
            conn.commit()
            player_1 = bot.send_message(us_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {usg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {crg.dice.value}\n❌ Вы проиграли {stavka} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            player_2 = bot.send_message(create_id, f"🗃 Результаты:\n\n👨🏼‍💻 Вы набрали очков {crg.dice.value}\n💁🏼‍♀️ Ваш оппонент набрал очков {usg.dice.value}\n🏆 Вы выиграли {win} RUB", reply_markup = menu_keyboard(us_id), parse_mode = "HTML")
            bot.send_message(admin, f"Получен процент с игры: {round(stavka*2 - win, 1)} RUB")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {usg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {crg.dice.value} очка(ов)\n\nИгрок @{player_2.chat.username} выиграл {win} RUB')
            cursor.execute(f"SELECT top_win FROM apple WHERE user_id = {create_id}")
            top_win = cursor.fetchone()[0]
            if win > top_win:
              cursor.execute(f"UPDATE apple SET top_win = {win} WHERE user_id = {create_id}")
              conn.commit()
          if usg.dice.value == crg.dice.value:  
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET balance = balance + {stavka} WHERE user_id = {create_id}")
            conn.commit()
            player_1 = bot.send_photo(create_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_avtomat_buttons(), parse_mode = "HTML")
            player_2 = bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption = f"Ничья!\nСтавки возвращены на баланс", reply_markup = list_avtomat_buttons(), parse_mode = "HTML")
            bot.edit_message_text(chat_id = chats, message_id = message_id, text = f'Результаты игры #{game_id}:\nИгрок @{player_1.chat.username}: {crg.dice.value} очка(ов) \nИгрок @{player_2.chat.username}: {usg.dice.value} очка(ов)\n\nНичья! Ставки возвращены на баланс')        
        else:
          bot.send_message(us_id, text=f"Недостаточно средств", reply_markup=menu_keyboard(us_id))
      except:
        bot.send_photo(us_id, photo = 'https://imgur.com/lJmJZSV', caption =f"✖️ Игра была закончена\n⚽ Выберите другую игру или создайте её сами", reply_markup=list_avtomat_buttons())
  
    if call.data.startswith('bot_'):
      game_name = call.data[4:]
      balance = get_user_balance(us_id)
      start = InlineKeyboardMarkup(row_width = 1)
      btn1 = InlineKeyboardButton(text = '🤪 Понятно', callback_data = f'start_robot_game{game_name}')
      btn2 = InlineKeyboardButton(text = '◀️ Назад', callback_data = 'pvp_games')
      start.add(btn1, btn2)
      bot.edit_message_caption(chat_id=call.message.chat.id, message_id = call.message.message_id, caption=f'🤖 <b>Игры с ботом проходят без ставок и созданы чтобы весело провести время!</b>', reply_markup=start, parse_mode = 'HTML')
      #bot.register_next_step_handler(msg, start_robot, game_name = game_name, rg = 1)
  
  
      #bot.forward_message(chat_id = create_id, from_chat_id = usg.chat.id, message_id=usg.message_id)
      #bot.send_message(create_id,f'Игрок @{call.from_user.username} присоеденился к игре!\nИгра №{game_id}\nCтавка: {stavka} RUB\n\n Ждём пока он бросит кубик...')
    if call.data.startswith('start_robot_game'):
    	bot.delete_message(chat_id=call.message.chat.id, message_id = call.message.message_id)
    	game_name = call.data[16:]
    	func_start_bot_game(us_id, game_name)
  
  
    if call.data == 'mines':
      cursor.execute("SELECT game_status FROM apple WHERE user_id = (?)", (us_id,))
      game_status = cursor.fetchone()[0]
      if game_status != 1111111110:
        msg = bot.send_message(us_id, text=f'✏️ Введите количество мин (от 3 до 24)', reply_markup = mines_kolv_keyboard)
        bot.register_next_step_handler(msg, get_mines)
      else:
        bot.send_message(us_id, text = '❌ Завершите предыдущую игру прежде чем начать новую', reply_markup = menu_keyboard(us_id))
  
    if call.data.startswith('mines_'):
      try:
        mine_3 = [1.1, 1.26, 1.45, 1.68, 1.96, 2.3, 2.73, 3.28, 3.98, 4.9, 6.13, 7.8, 10.14, 13.52, 18.59, 26.56, 39.84, 63.74, 111.55, 223.1, 557.75, 2230]
        mine_4 = [1.15, 1.39, 1.68, 2.05, 2.53, 3.17, 4.01, 5.16, 6.74, 8.99, 12.26, 17.16, 24.79, 37.18, 58.43, 97.38, 175.29, 350.58, 818.03, 2450, 12270]
        mine_5 = [1.21, 1.53, 1.96, 2.53, 3.32, 4.43, 6.01, 8.33, 11.8, 17.16, 25.74, 40.04, 65.07, 111.55, 204.51, 409.02, 920.29, 2450, 8590, 51240]
        mine_6 = [1.28, 1.7, 2.3, 3.17, 4.43, 6.33, 9.25, 13.88, 21.45, 34.32, 57.2, 100.11, 185.92, 371.83, 818.03, 2050, 6140, 24540, 172000]
        mine_7 = [1.35, 1.9, 2.73, 4.01, 6.01, 9.25, 14.65, 23.98, 40.76, 72.46, 135.86, 271.72, 588.74, 1410, 3890, 12950, 58280, 466000,]
        mine_8 = [1.43, 2.14, 3.28, 5.16, 8.33, 13.88, 23.98, 43.16, 81.52, 163.03, 349.36, 815.17, 2120, 6360, 23310, 117000, 1000000]
        mine_9 = [1.51, 2,42, 3.98, 6.74, 11.8, 21.45, 40.76, 81.52, 173.22, 395.94, 989.85, 2770, 9010, 36030, 198000, 1980000]
        mine_10 = [1.62, 2.77, 4.9, 8.9, 17, 34, 72, 163, 395, 1000, 3170, 11090, 48000, 288000, 3170000]
        mine_11 = [1.73, 3.2, 6.1, 12.2, 25.7, 57.2, 135, 349, 989, 3170, 11880, 55430, 360000, 4320000]
        mine_12 = [1.86, 3.7, 7.8, 17.1, 40, 100, 271, 815, 2700, 11000, 55000, 388000, 5000000]
        mine_13 = [2.02, 4.4, 10.14, 24.7, 65, 185, 588, 2120, 9001, 48040, 360000, 5000000]
        mine_14 = [2.2, 5.29, 13.52, 37.18, 111.55, 371.83, 1410, 6360, 36030, 288000, 4000000]
        mine_15 = [2.42, 6.47, 18.5, 58.43, 204, 818, 3890, 23310, 198000, 3170000]
        mine_16 = [2.69, 8, 26, 97, 409, 2050, 12950, 117000, 1980000]
        mine_17 = [3, 10, 39, 175, 920, 6140, 58280, 1000000]
        mine_18 = [3.46, 13.8, 63, 350, 2450, 24540, 466000]
        mine_19 = [4.04, 19.4, 111.5, 818, 8590, 172000]
        mine_20 = [4.85, 29.1, 223.1, 2450, 51400]
        mine_21 = [6, 48.5, 557, 12270]
        mine_22 = [8, 97, 2230]
        mine_23 = [12.1, 291]
        mine_24 = [24.9]
        cursor.execute("SELECT mines_map_buttons FROM apple WHERE user_id = ('%s')"%(us_id,))
        myresult = cursor.fetchone()
        data = json.loads(myresult[0])
        if data[call.data] != '💎':
          cursor.execute("SELECT now_stavka FROM apple WHERE user_id = ('%s')"%(us_id,))
          stavka = cursor.fetchone()[0]
          cursor.execute("SELECT kassa FROM settings WHERE bot = 1")
          kassa = cursor.fetchone()[0]
          cursor.execute("SELECT now_state FROM apple WHERE user_id = ('%s')"%(us_id,))
          now_state = cursor.fetchone()[0]
          cursor.execute("SELECT how_mines FROM apple WHERE user_id = ('%s')"%(us_id,))
          mines_kolv = cursor.fetchone()[0]
          cursor.execute("SELECT antiminus FROM settings WHERE bot = 1")
          antiminus = cursor.fetchone()[0]
          cursor.execute("SELECT win_money FROM apple WHERE user_id = ('%s')"%(us_id,))
          last_win_money = cursor.fetchone()[0]
          x = eval(f"mine_{mines_kolv}[{now_state}]")
          try:
            next_x = eval(f"mine_{mines_kolv}[{now_state + 1}]")
          except:
            next_x = 0 
          now_state = now_state + 1
          next_money = round(stavka *next_x, 2)
          win_money = round(stavka *x, 2)
          choice = random.randint(0,4)
          cursor.execute('SELECT podkrutka FROM apple WHERE user_id = (?)', (us_id,))
          podkrutka_user = cursor.fetchone()[0]
          cursor.execute('SELECT all_podkrutka FROM settings WHERE bot = 1')
          podkrutka_all = cursor.fetchone()[0]
          if kassa - (win_money + last_win_money) > antiminus and choice != 1 or podkrutka_user == 1 or podkrutka_all == 1:
            
            new_kassa = (kassa - win_money) + last_win_money
            cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
            conn.commit()
            data[call.data] = '💎'
            mines_keyboard = types.InlineKeyboardMarkup(row_width=5)
            button_list = [types.InlineKeyboardButton(text=text, callback_data=cd) for cd, text in data.items()]
            close_game = types.InlineKeyboardButton(text=f'❌ Забрать {win_money} RUB ', callback_data='close_game')   
            mines_keyboard.add(*button_list, close_game)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'💰 Ставка - {stavka} RUB\n🏆 Текущий выигрыш - {win_money} RUB (x{x})\n🏆 Следущий выигрыш - {next_money} RUB (x{next_x})', reply_markup=mines_keyboard)
            func_mines_map(user_id=us_id, mines_map=data, now_stavka=stavka, now_x = x, now_state = now_state, win_money = win_money )
  
          else:
            cursor.execute("SELECT win_money FROM apple WHERE user_id = ('%s')"%(us_id,))
            win_money = cursor.fetchone()[0]
            cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
            cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
            conn.commit()
            data[call.data] = '💣'
            cursor.execute("SELECT priglasil_id FROM apple WHERE user_id = (?)",[call.from_user.id])
            priglasil_id = cursor.fetchone()[0]
            if priglasil_id != None:
              try:
                cursor.execute('SELECT partner FROM apple WHERE user_id = (?)', (priglasil_id,))
                partner = cursor.fetchone()[0]
                if partner == 1:
                  cursor.execute('SELECT how_procent FROM apple WHERE user_id = (?)', (priglasil_id,))
                  procent = cursor.fetchone()[0]
                  money = round(stavka/100 * procent, 2)
                  cursor.execute(f'UPDATE apple SET balance = balance + {money} WHERE user_id = (?)', (priglasil_id,))
                  balance_partner = get_user_balance(priglasil_id)
                  bot.send_message(priglasil_id, text = f'✅ Получено: {money} RUB\n💰 Ваш баланс: {balance_partner} RUB')
                  new_kassa = kassa + win_money - (stavka - (stavka - money))
                  cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                  conn.commit()
                else:
                  new_kassa = kassa + win_money
                  cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                  conn.commit()  
              except:
                new_kassa = kassa + win_money
                cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                conn.commit()
            else:
              new_kassa = kassa + win_money
              cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
              conn.commit()
  
            mines_keyboard = types.InlineKeyboardMarkup(row_width=5)
            button_list = [types.InlineKeyboardButton(text=text, callback_data='lose') for cd, text in data.items()]
            close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='menu')
            repeat_game = types.InlineKeyboardButton(text='🔄 Ещё раз', callback_data='repeat_mines')
            cursor.execute("UPDATE apple SET all_game_apple = all_game_apple + 1 WHERE user_id = ('%s')"%(us_id,))
            cursor.execute(f'UPDATE apple SET game_status = 0 WHERE user_id = {us_id}')
            conn.commit()
            mines_keyboard.add(*button_list, repeat_game)
            mines_keyboard.add(close_game)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'Вы проиграли', reply_markup=mines_keyboard)
  
  
      except Exception as e:
        cursor.execute("SELECT mines_map_buttons FROM apple WHERE user_id = ('%s')"%(us_id,))
        myresult = cursor.fetchone()
        data = json.loads(myresult[0])
        mines_keyboard = types.InlineKeyboardMarkup(row_width=5)
        button_list = [types.InlineKeyboardButton(text=text, callback_data=cd) for cd, text in data.items()]
        close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='close_game')     
        mines_keyboard.add(*button_list, close_game)
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'Вы разгадали всё клетки!\nНажмите "❌ Закончить игру" чтобы забрать выигрыш!',reply_markup=mines_keyboard)
  
  #2.7 2.3 2.0 1.7 1.5 1.3
  
  
    if call.data == 'apple':
      cursor.execute("SELECT game_status FROM apple WHERE user_id = (?)", (us_id,))
      game_status = cursor.fetchone()[0]
      if game_status != 11111110:
        balance = get_user_balance(us_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup=stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'apple')
      else:
        bot.send_message(us_id, text = '❌ Завершите предыдущую игру прежде чем начать новую', reply_markup = menu_keyboard(us_id))
  
  
    if call.data.startswith('key'):
      cursor.execute("SELECT now_state FROM apple WHERE user_id = ('%s')"%(us_id,))
      state = cursor.fetchone()
      cursor.execute("SELECT now_stavka FROM apple WHERE user_id = ('%s')"%(us_id,))
      stavka = cursor.fetchone()
      cursor.execute("SELECT kassa FROM settings WHERE bot = 1")
      kassa = cursor.fetchone()[0]
      cursor.execute('UPDATE settings SET promej_kassa = (?) where bot = 1', (kassa,))
      conn.commit()
      now_stavka = int(stavka[0])
      state = int(state[0])
      if int(call.data[3]) == state:
  
        us_id = call.from_user.id
  
        #кнопки яблок
        cursor.execute("SELECT map_buttons FROM apple WHERE user_id = ('%s')"%(us_id,))
        myresult = cursor.fetchone()
  
        #Множитель x
        cursor.execute("SELECT now_x FROM apple WHERE user_id = ('%s')"%(us_id,))
        x = cursor.fetchone()
        cursor.execute("SELECT now_stavka FROM apple WHERE user_id = ('%s')"%(us_id,))
        stavka = int(cursor.fetchone()[0])
        now_x = round(x[0], 2)
        next_x = round((x[0] * 1.25), 2)
        now = round(now_x * float(stavka), 2)
        nextt = round(next_x * float(stavka), 2)
  
        #Ступень
        cursor.execute("SELECT now_state FROM apple WHERE user_id = ('%s')"%(call.from_user.id,))
        step = cursor.fetchone()
        step = int(step[0])
        step =step + 1
        conn.commit()
        data = json.loads(myresult[0])
        cursor.execute("SELECT win_money FROM apple WHERE user_id = (?)",[us_id,])
        win_money = cursor.fetchone()[0]
        cursor.execute("SELECT antiminus FROM settings WHERE bot = 1")
        antiminus = cursor.fetchone()[0]
        conn.commit()
        cursor.execute("SELECT promej_kassa FROM settings WHERE bot = 1")
        promej_kassa = cursor.fetchone()[0]
        conn.commit()
        last_x = (now)/1.25 if now_x !=1.25 else stavka
  
        #Антиминус (Маржа)
        choice = random.randint(0,1)
        cursor.execute('SELECT podkrutka FROM apple WHERE user_id = (?)', (us_id,))
        podkrutka_user = cursor.fetchone()[0]
        cursor.execute('SELECT all_podkrutka FROM settings WHERE bot = 1')
        podkrutka_all = cursor.fetchone()[0]
        if kassa - now + last_x > antiminus and choice == 1 or podkrutka_user == 1 or podkrutka_all == 1:
          new_kassa = round((kassa - now) + last_x)
          data[call.data] = '🍏'
          cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
          conn.commit()
          apple_keyboard = types.InlineKeyboardMarkup(row_width=5)
          button_list = [types.InlineKeyboardButton(text=text, callback_data=cd) for cd, text in data.items()]
          close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='close_game')     
          apple_keyboard.add(*button_list, close_game)
          bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'🍏 Текущий выигрыш: {now} RUB (x{now_x})\n\n🍎 Следущий выигрыш: {nextt} RUB (x{next_x})', reply_markup=apple_keyboard)
          func_apple_map(user_id=us_id, apples_map=data, now_state=step, now_x = next_x, now_stavka=now_stavka, win_money = now)
        else:
          data[call.data] = '💣'
          cursor.execute(f"UPDATE apple SET all_lose = all_lose + {stavka} WHERE user_id = {us_id}")
          conn.commit()
          cursor.execute(f"UPDATE apple SET game_lose = game_lose + 1 WHERE user_id = {us_id}")
          cursor.execute("SELECT priglasil_id FROM apple WHERE user_id = (?)",[call.from_user.id])
          priglasil_id = cursor.fetchone()[0]
          if priglasil_id != None:
            try:
              cursor.execute('SELECT partner FROM apple WHERE user_id = (?)', (priglasil_id,))
              partner = cursor.fetchone()[0]
              if partner == 1:
                cursor.execute('SELECT how_procent FROM apple WHERE user_id = (?)', (priglasil_id,))
                procent = cursor.fetchone()[0]
                procent = int(procent)
                money = round(stavka/100 * procent, 2)
  
                cursor.execute(f'UPDATE apple SET balance = balance + {money} WHERE user_id = (?)', (priglasil_id,))
                conn.commit()
                balance_partner = get_user_balance(priglasil_id)
                bot.send_message(priglasil_id, text = f'✅ Получено: {money} RUB\n💰 Ваш баланс: {balance_partner} RUB')
                new_kassa = kassa + win_money - (stavka - (stavka - money))
                cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                conn.commit()
              else:
                new_kassa = kassa + win_money
                cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                conn.commit()  
            except Exception as e:
              new_kassa = kassa + win_money
              cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
              conn.commit()
          else:
            new_kassa = kassa + win_money
            cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
            conn.commit()
          apple_keyboard = types.InlineKeyboardMarkup(row_width=5)
          button_list = [types.InlineKeyboardButton(text=text, callback_data='lose') for cd, text in data.items()]
          close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='menu')
          repeat_game = types.InlineKeyboardButton(text='🔄 Ещё раз', callback_data='repeat_apple')
          apple_keyboard.add(*button_list, repeat_game)
          apple_keyboard.add(close_game)
          bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption = f'Вы проиграли', reply_markup=apple_keyboard)
  
  
    if call.data.startswith('repeat_'):
      game = call.data[7:]
      bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
      balance = get_user_balance(us_id)
      if game == 'mines':
        msg = bot.send_message(us_id, text=f'✏️ Введите количество мин (от 3 до 24)', reply_markup = mines_kolv_keyboard)
        bot.register_next_step_handler(msg, get_mines)
      else:
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup = stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = game)
  
    if call.data == 'triple':
      cursor.execute("SELECT game_status FROM apple WHERE user_id = (?)", (us_id,))
      game_status = cursor.fetchone()[0]
      if game_status != 111111110:
        us_id = call.from_user.id
        balance = get_user_balance(us_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.message.chat.id, text=f'✏️ Введите ставку\n💰 Ваш баланс: {balance} RUB', reply_markup = stavka_keyboard(us_id))
        bot.register_next_step_handler(msg, get_stavka, game_name = 'triple')
      else:
        bot.send_message(us_id, text = '❌ Завершите предыдущую игру прежде чем начать новую', reply_markup = menu_keyboard(us_id))
  
    if call.data == 'dice_B2':
  
      us_id = call.from_user.id
      cursor.execute("SELECT triple_map_buttons FROM apple WHERE user_id = ('%s')"%(us_id, ))
      myresult = cursor.fetchone()
      cursor.execute("SELECT now_stavka FROM apple WHERE user_id = ('%s')"%(us_id,))
      stavka = cursor.fetchone()[0]
      cursor.execute("SELECT kassa FROM settings WHERE bot = 1")
      kassa = cursor.fetchone()[0]
      cursor.execute("SELECT balance FROM apple WHERE user_id = (?)",[call.from_user.id])
      balance = cursor.fetchone()[0]
      cursor.execute("SELECT antiminus FROM settings WHERE bot = 1")
      antiminus = cursor.fetchone()[0]
      conn.commit()
      cursor.execute('SELECT podkrutka FROM apple WHERE user_id = (?)', (us_id,))
      podkrutka_user = cursor.fetchone()[0]
      cursor.execute('SELECT all_podkrutka FROM settings WHERE bot = 1')
      podkrutka_all = cursor.fetchone()[0]
      if balance >= stavka:
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "⚽️")
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "⚽️🏀")
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "⚽️🏀🎾")
        data = json.loads(myresult[0])
        choice = random.randint(0,7)
  
        if kassa - (stavka * 80) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 0 or podkrutka_all == 1 and choice == 0:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '🎾'
          data['dice_B3'] = '🎾'
          data['dice_C2'] = 'x80'
          win_money = stavka * 80
          x = 80
  
        elif kassa - (stavka * 30) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 1 or podkrutka_all == 1 and choice == 1:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '🎾'
          data['dice_B3'] = '🏀'
          data['dice_C2'] = 'x30'
          win_money = stavka * 30
          x = 30
  
        elif kassa - (stavka * 15) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 2 or podkrutka_all == 1 and choice == 2:
          data['dice_A2'] = '🏀'
          data['dice_B1'] = '🏀'
          data['dice_B3'] = '🏀'
          data['dice_C2'] = 'x15'
          win_money = stavka * 15
          x = 15
  
        elif kassa - (stavka * 10) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 3 or podkrutka_all == 1 and choice == 3:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '🏀'
          data['dice_B3'] = '🏀'
          data['dice_C2'] = 'x10'
          win_money = stavka * 10
          x = 10
  
        elif kassa - (stavka * 6.7) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 4 or podkrutka_all == 1 and choice == 4:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '🎾'
          data['dice_B3'] = '⚽️'
          data['dice_C2'] = 'x6.7'
          win_money = stavka * 6.7
          x = 6.7
  
        elif kassa - (stavka * 3) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 5 or podkrutka_all == 1 and choice == 5:
          data['dice_A2'] = '🏀'
          data['dice_B1'] = '🏀'
          data['dice_B3'] = '⚽️'
          data['dice_C2'] = 'x3'
          win_money = stavka * 3
          x = 3
  
        elif kassa - (stavka * 2.4) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 6 or podkrutka_all == 1 and choice == 6:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '🏀'
          data['dice_B3'] = '⚽️'
          data['dice_C2'] = 'x2.4'
          win_money = stavka * 2.4
          x = 2.4
  
        elif kassa - (stavka * 1.5) > antiminus and choice != 1 or podkrutka_user == 1 and choice == 7 or podkrutka_all == 1 and choice == 7:
          data['dice_A2'] = '🎾'
          data['dice_B1'] = '⚽️'
          data['dice_B3'] = '⚽️'
          data['dice_C2'] = 'x1.5'
          win_money = stavka * 1.5
          x = 1.5
  
        else:
          data['dice_A2'] = '⚽️'
          data['dice_B1'] = '⚽️'
          data['dice_B3'] = '⚽️'
          data['dice_C2'] = 'x0'
          win_money = stavka
          x = 0
        if x == 0:
          cursor.execute(f'UPDATE apple SET balance = balance - {win_money} where user_id = (?)', [call.from_user.id,])
          conn.commit()
          cursor.execute("SELECT priglasil_id FROM apple WHERE user_id = (?)",[call.from_user.id])
          priglasil_id = cursor.fetchone()[0]
          if priglasil_id != None:
            try:
              cursor.execute('SELECT partner FROM apple WHERE user_id = (?)', (priglasil_id,))
              partner = cursor.fetchone()[0]
              if partner == 1:
                cursor.execute('SELECT how_procent FROM apple WHERE user_id = (?)', (priglasil_id,))
                procent = cursor.fetchone()[0]
                money = round(stavka/100 * procent, 2)
                cursor.execute(f'UPDATE apple SET balance = balance + {money} WHERE user_id = (?)', (priglasil_id,))
                balance_partner = get_user_balance(priglasil_id)
                bot.send_message(priglasil_id, text = f'✅ Получено: {money} RUB\n💰 Ваш баланс: {balance_partner} RUB')
                new_kassa = kassa + (win_money - money)
                cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                conn.commit()
                win_money = 0
              else:
                new_kassa = kassa + win_money
                cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
                conn.commit()              
            except Exception as e:
              new_kassa = kassa + win_money
              cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
              conn.commit()
              win_money = 0
          else:
            new_kassa = kassa + win_money
            cursor.execute('UPDATE settings SET kassa = (?)  where bot = 1', (new_kassa,))
            conn.commit()
            win_money = 0
        else:
          cursor.execute(f'UPDATE apple SET balance = balance + {win_money} where user_id = ?', [call.from_user.id,])
          cursor.execute(f'UPDATE settings SET kassa = kassa - {win_money} where bot = 1')
          conn.commit()
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      messagetoedit = bot.send_message(chat_id=call.message.chat.id, text = data['dice_B1'])
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=messagetoedit.message_id, text = data['dice_B1']+data['dice_A2'])
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=messagetoedit.message_id, text = data['dice_B1']+data['dice_A2']+data['dice_B3'])
      cursor.execute(f'UPDATE apple SET all_game_triple = all_game_triple + 1 where user_id = {us_id}')
      conn.commit()
      start_triple_keyboard1 = types.InlineKeyboardMarkup(row_width=3)
      button_list = [types.InlineKeyboardButton(text=text, callback_data=cd) for cd, text in data.items()]
      repeat_game = types.InlineKeyboardButton(text = '🔄 Изменить ставку', callback_data = 'repeat_triple')
      close_game = types.InlineKeyboardButton(text='❌ Закончить игру', callback_data='menu')     
      start_triple_keyboard1.add(*button_list, repeat_game)
      start_triple_keyboard1.add(close_game)
      bot.delete_message(chat_id=call.message.chat.id, message_id=messagetoedit.message_id)
      bot.send_photo(chat_id=call.message.chat.id,photo = 'https://sun9-6.userapi.com/impg/4If-zqfmPzNODc5o9b_-k38UURuut7_1XfBSNg/V_qpdCSomJ8.jpg?size=1000x400&quality=96&sign=df314ec3aa3f33b67434df9c3c7b4df0&type=album', caption = f"🚀 Ваша ставкa: {stavka} RUB\n\n🏆 Ваш выигрыш: {win_money} RUB (x{x})\n\n💰 Баланс: {balance + win_money} RUB", reply_markup=start_triple_keyboard1)
  
    if call.data == 'close_game':
      cursor.execute("SELECT win_money FROM apple WHERE user_id = (?)",[call.from_user.id])
      win_money = cursor.fetchone()[0]
      cursor.execute('UPDATE apple SET balance = balance + win_money where user_id = (?)', [call.from_user.id])
      cursor.execute('UPDATE apple SET all_win = all_win + win_money where user_id = (?)', [call.from_user.id])
      cursor.execute('UPDATE apple SET win_money = "0" where user_id = ?', [call.from_user.id])
      cursor.execute("UPDATE apple SET game_status = 0 WHERE user_id = (?)", (us_id,))
      cursor.execute(f"UPDATE apple SET all_win = all_win + {win_money} WHERE user_id = {us_id}")
      cursor.execute(f"UPDATE apple SET game_win = game_win + 1 WHERE user_id = {us_id}")
      conn.commit()
      cursor.execute('SELECT top_win FROM apple WHERE user_id = (?)', (us_id,))
      top_win = cursor.fetchone()[0]
      if win_money > top_win:
        cursor.execute(f"UPDATE apple SET top_win = {win_money} WHERE user_id = {us_id}")
        conn.commit()
      
      balance = get_user_balance(us_id)
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      bot.send_photo(chat_id=call.message.chat.id,photo = 'https://imgur.com/lJmJZSV', caption = f'<b>📍 Игра окончена!</b>\n🏆Вы выйграли {win_money} RUB\n💰 Ваш баланс: {balance} RUB', reply_markup=menu_keyboard(us_id),parse_mode = 'HTML')
  
    if call.data == 'menu':
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      cursor.execute("UPDATE apple SET game_status = 0 WHERE user_id = (?)", (us_id,))
      conn.commit()
      glav_message(us_id)
  
  
    if call.data == 'check_payment':
      conn = sqlite3.connect('database.db', check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute("SELECT pay_id FROM apple WHERE user_id = (?)",[call.from_user.id])
      qid = cursor.fetchone()[0]
      cursor.execute("SELECT p2p_key FROM settings WHERE bot = 1")
      KEY = cursor.fetchone()[0]
      p2p = QiwiP2P(auth_key=KEY)
      status =p2p.check(bill_id=qid).status
  
      if status == 'PAID':
        bot.delete_message(chat_id = us_id, message_id = call.message.message_id)
        cursor.execute("SELECT pay_sum FROM apple WHERE user_id = (?)",[call.from_user.id])
        pay = cursor.fetchone()[0]
  
        cursor.execute("SELECT balance FROM apple WHERE user_id = (?)",[call.from_user.id])
        balance = cursor.fetchone()[0]
        new_balance = balance + pay
        cursor.execute('UPDATE apple SET balance = (?) where user_id = (?)', (new_balance, us_id))
        cursor.execute(f'UPDATE settings SET all_deposit = all_deposit + {pay} where bot = 1')
        cursor.execute(f'UPDATE apple SET how_deposit = how_deposit + {pay} where user_id = (?)', (us_id,))
        conn.commit()
        #cursor.execute("SELECT p2p_key FROM settings WHERE bot = 1")
        #KEY = cursor.fetchone()[0]
        cursor.execute('UPDATE apple SET pay_id = 0 where user_id = (?)', (us_id,))
        cursor.execute("SELECT username FROM apple WHERE user_id = (?)", (us_id,))
        cursor.execute(f'UPDATE apple SET how_deposit = how_deposit + {pay} where user_id = (?)', (us_id,))
        conn.commit()
        cursor.execute("SELECT username FROM apple WHERE user_id = (?)", (us_id,))
        paid_user = cursor.fetchone()[0]
        cursor.execute("SELECT priglasil_id FROM apple WHERE user_id = (?)",[call.from_user.id])
        priglasil_id = cursor.fetchone()[0]
        if priglasil_id != None:
          cursor.execute('SELECT partner FROM apple WHERE user_id  = (?)', (priglasil_id,))
          partner = cursor.fetchone()[0]
          if partner != 1:
            ref_pay = pay/100*5
            cursor.execute(f'UPDATE apple SET balance = balance + {ref_pay} where user_id = (?)', (priglasil_id,))
            cursor.execute(f'UPDATE apple SET referal_money = referal_money + {ref_pay} where user_id = (?)', (priglasil_id,))
            conn.commit()
            bot.send_message(priglasil_id, text = f'🎁 Вы получили {ref_pay} RUB за пополнение реферала!', reply_markup = close_message_keyboard)
            bot.send_message(channel_id, text = f'🕹 @{paid_user} пополнил баланс на {pay}₽')
        bot.send_message(chat_id=call.message.chat.id, text=f'Ваш баланс пополнен на {pay}₽', reply_markup=None)
        glav_message(us_id)
  
  
    if call.data == 'undo_payment':
      conn = sqlite3.connect('database.db', check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute("SELECT pay_id FROM apple WHERE user_id = (?)",[call.from_user.id])
      qid = cursor.fetchone()[0]
      cursor.execute("SELECT p2p_key FROM settings WHERE bot = 1")
      KEY = cursor.fetchone()[0]
      p2p = QiwiP2P(auth_key=KEY)
      p2p.reject(bill_id=qid)
      status =p2p.check(bill_id=qid).status
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
      bot.send_message(chat_id=call.message.chat.id, text=f'Пополнение отменено', reply_markup=None)
      glav_message(us_id)
  
    if call.data == 'ya_soglasen':
      try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        glav_message(us_id)
      except:
        pass
  
    if call.data.startswith('viplatit'):
      player_id = call.data[8:]
      conn = sqlite3.connect('database.db', check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute("SELECT username FROM apple WHERE user_id = (?)",[player_id])
      username = cursor.fetchone()[0]
      cursor.execute("UPDATE apple SET vivod = 0 WHERE user_id = (?)",[player_id])
      conn.commit()
      cursor.execute("SELECT partner FROM apple WHERE user_id = (?)",[player_id])
      partner = cursor.fetchone()[0]
      cursor.execute("SELECT summa_vivoda FROM apple WHERE user_id = (?)",[player_id])
      summa = cursor.fetchone()[0]
      cursor.execute("SELECT top_vivod FROM apple WHERE user_id = (?)",[player_id])
      top_vivod = cursor.fetchone()[0]
      cursor.execute('UPDATE apple SET how_vivod = how_vivod + (?) WHERE user_id = (?)', (summa, player_id))
      conn.commit()
      cursor.execute('UPDATE apple SET top_vivod = top_vivod + (?) WHERE user_id = (?)', (summa, player_id))
      conn.commit()
      bot.send_message(player_id, text = f'<b>✅ Заявка на вывод одобрена</b>\n\n<i>📥 Деньги поступят в течении 10 минут</i>', reply_markup = menu_keyboard(player_id), parse_mode = 'HTML')
      bot.send_message(chats, f"<b>✅ Вывод отправлен!</b>!\n\n<i>👨‍💻 Пользователь: @{username}\n💰 Сумма: {summa} RUB</i>", parse_mode = "HTML")
      if partner  == 1:
        bot.edit_message_reply_markup(chat_id=parner_channel, message_id=call.message.message_id, reply_markup=viplacheno_keyboard)
      else:
        bot.edit_message_reply_markup(chat_id=us_id, message_id=call.message.message_id, reply_markup=viplacheno_keyboard)
  
  
    if call.data.startswith('otklonit'):
      player_id = call.data[8:]
      conn = sqlite3.connect('database.db', check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute("SELECT username FROM apple WHERE user_id = (?)",[player_id])
      username = cursor.fetchone()[0]
      cursor.execute("UPDATE apple SET vivod = 0 WHERE user_id = (?)",[player_id])
      cursor.execute("UPDATE apple SET balance = balance + summa_vivoda WHERE user_id = (?)",[player_id])
      conn.commit()
      cursor.execute("SELECT partner FROM apple WHERE user_id = (?)",[player_id])
      partner = cursor.fetchone()[0]
      bot.send_message(player_id, text = f'<b>❌ Заявка на вывод отклонена</b>', reply_markup = menu_keyboard(player_id), parse_mode = 'HTML')
      if partner  == 1:
        bot.edit_message_reply_markup(chat_id=parner_channel, message_id=call.message.message_id, reply_markup=otkloneno_keyboard)
      else:
        bot.edit_message_reply_markup(chat_id=us_id, message_id=call.message.message_id, reply_markup=otkloneno_keyboard)
  
    if call.data == 'close_message':
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  
    if call.data == 'otmena':
      glav_menu(us_id)
    if call.data == 'back_popol':
      msg = bot.send_message(us_id, f"💰 Выберите метод оплаты\n⚠️ Минимальная сумма - 10 RUB", reply_markup=vibor_plata_keyboard)
      bot.register_next_step_handler(msg, vibor_plata)
  
    if call.data.startswith('check_crystal_'):
      cursor.execute("SELECT crystal_key FROM settings WHERE bot = 1")
      key = cursor.fetchone()[0]
      cursor.execute("SELECT crystal_login FROM settings WHERE bot = 1")
      login =cursor.fetchone()[0]
      cursor.execute("SELECT pay_id FROM apple WHERE user_id = (?)",[us_id])
      pay_id =cursor.fetchone()[0]
      response = requests.get(url = f'https://api.crystalpay.ru/v1/?s={key}&n={login}&o=receipt-check&i={pay_id}')
      json_response = response.json()
      status = json_response['state']
      print(status)
      if status == 'payed':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        money = call.data[14:]
        balance = get_user_balance(us_id)
        new_balance = balance + int(money)
        cursor.execute('UPDATE apple SET balance = (?) where user_id = (?)', (new_balance, us_id))
        cursor.execute(f'UPDATE settings SET all_deposit = all_deposit + {money} where bot = 1')
        cursor.execute(f'UPDATE apple SET how_deposit = how_deposit + {money} where user_id = (?)', (us_id,))
        conn.commit()
        cursor.execute("SELECT priglasil_id FROM apple WHERE user_id = (?)",[call.from_user.id])
        priglasil_id = cursor.fetchone()[0]
        if priglasil_id != None:
          cursor.execute('SELECT partner FROM apple WHERE user_id  = (?)', (priglasil_id,))
          partner = cursor.fetchone()[0]
          if partner != 1:
            ref_pay = pay/100*5
            cursor.execute(f'UPDATE apple SET balance = balance + {ref_pay} where user_id = (?)', (priglasil_id,))
            cursor.execute(f'UPDATE apple SET referal_money = referal_money + {ref_pay} where user_id = (?)', (priglasil_id,))
            conn.commit()
            bot.send_message(priglasil_id, text = f'🎁 Вы получили {ref_pay} RUB за пополнение реферала!', reply_markup = close_message_keyboard)
        bot.send_message(channel_id, text = f'🕹 @{paid_user} пополнил баланс на {pay}₽')
        glav_message(us_id)
  else:
    pass







    







bot.polling(none_stop = True, interval = 0)