import telebot
from telebot import types
import pandas as pd 
import random2 as random
import pickle

bot = telebot.TeleBot('6719752669:AAEx6iwkPUkb8LZFqvF52dMgpJzj8OoVPmM')

global id_link_1
global id_link_2

def id_cleaner(girl_id):
    return 'https://ies.unitech-mo.ru/user?userid=' + str(girl_id)

def get_random_number(user_id):

    # Проверяем, есть ли состояние для данного пользователя
    if user_id in users_state:
        user_numbers = users_state[user_id]  # Получаем список выбранных чисел для пользователя
    else:
        user_numbers = []  # Создаем новый список выбранных чисел для пользователя
        users_state[user_id] = user_numbers  # Добавляем состояние для пользователя в словарь

    # Выбираем случайное число из общего списка значений
    random_girl_IDs = random.sample([i for i in range(0, len(df['Link'])) if i not in users_state.get(user_id, [])], 1)

    while random_girl_IDs in users_state.get(user_id, []):
        random_girl_IDs = random.sample([i for i in range(0, len(df['Link'])) if i not in users_state.get(user_id, [])], 1)
    else:   
        # Добавляем выбранные числа в список выбранных чисел для пользователя
        user_numbers.extend(random_girl_IDs)

    # Обновление словаря в файле
    with open('users_state.pickle', 'wb') as users_state_log:
        pickle.dump(users_state, users_state_log)

    # Возвращаем выбранные числа
    return list(df.iloc[random_girl_IDs].squeeze())
    

@bot.message_handler(commands=['start']) 
def start(message): # message -- вся инфа о пользователе в виде словаря
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📊Статистика') 
    btn2 = types.KeyboardButton('🥰Перейти к сравнению') 
    btn3 = types.KeyboardButton('📋Правила') 
    btn4 = types.KeyboardButton('💌Пожелания') 
    markup.add(btn1, btn2, btn3, btn4) # добавить кнопки в меню
    bot.send_message(message.chat.id, "Привет, этот бот создан с целью определить самую красивую девушку в нашем университете.", reply_markup=markup) 
    bot.register_next_step_handler(message, on_click_menu)

def on_click_menu(message):
    global id_link_1
    global id_link_2

    if message.text == '📊Статистика':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('↩️ Назад')
        markup.add(btn3)
        bot.send_message(message.chat.id, "Здесь будет список самый красивых девушек отсортированных по рейтингу.", reply_markup=markup) 
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '🥰Перейти к сравнению':
        
        # Задаем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('◀️ Левая') 
        btn2 = types.KeyboardButton('▶️ Правая')
        btn3 = types.KeyboardButton('↩️ Назад')
        markup.add(btn1, btn2, btn3) # добавить кнопки в меню

        # создаем список с types файлов и ссылками на фото
        id_link_1 = get_random_number(message.from_user.id)
        id_link_2 = get_random_number(message.from_user.id)    

        # Составим список из фото
        photos = [types.InputMediaPhoto(id_link_1[0]), types.InputMediaPhoto(id_link_2[0])] 

        # Отправляем 2 фото и фразу сравнения
        bot.send_media_group(message.chat.id, photos) 
        bot.send_message(message.from_user.id, 
        f"<a href='{id_cleaner(id_link_1[3])}'>{id_link_1[2]}</a> или<a href='{id_cleaner(id_link_2[3])}'>{id_link_2[2]}</a>?",
        parse_mode='HTML', reply_markup=markup) 

        # Переход к дейсвию после нажатия
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '📋Правила':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('↩️ Назад')
        markup.add(btn3)
        bot.send_message(message.chat.id, 
        "Тебе показывают фото двух девушек, ты должен нажать на стрелку указывающую на девушку, которая тебе больше понравилась. Нажав на имя ты можешь перейти на профиль девушки на нашем портале.", reply_markup=markup) 
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '💌Пожелания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.InlineKeyboardMarkup()
        btn3 = types.KeyboardButton('↩️ Назад')
        btn4 = types.InlineKeyboardButton(text='💌 Отправить сообщение!', url='https://t.me/+B5CscsllxBk5MTMy')
        keyboard.add(btn4)
        markup.add(btn3)
        bot.send_message(message.chat.id, "Для ваших пожеланий я создал отдельный канал.", reply_markup=markup) 
        bot.send_message(message.chat.id, "Просто напиши, что хочешь в чат одним сообщеним.", reply_markup=keyboard)
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '◀️ Левая':
       # Задаем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('◀️ Левая') 
        btn2 = types.KeyboardButton('▶️ Правая')
        btn3 = types.KeyboardButton('↩️ Назад')
        markup.add(btn1, btn2, btn3) # добавить кнопки в меню

        # создаем список с types файлов и ссылками на фото
        id_link_2 = get_random_number(message.from_user.id)
        photos = [types.InputMediaPhoto(id_link_1[0]),
        types.InputMediaPhoto(id_link_2[0])] 

        # Отправляем 2 фото и фразу сравнения
        bot.send_media_group(message.chat.id, photos) 
        bot.send_message(message.from_user.id, 
        f"<a href='{id_cleaner(id_link_1[3])}'>{id_link_1[2]}</a> или<a href='{id_cleaner(id_link_2[3])}'>{id_link_2[2]}</a>?", 
        parse_mode='HTML', reply_markup=markup)

        # Переход к дейсвию после нажатия
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '▶️ Правая':
        # Задаем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('◀️ Левая') 
        btn2 = types.KeyboardButton('▶️ Правая')
        btn3 = types.KeyboardButton('↩️ Назад')
        markup.add(btn1, btn2, btn3) # добавить кнопки в меню

        # создаем список с types файлов и ссылками на фото
        id_link_1 = get_random_number(message.from_user.id)
        photos = [types.InputMediaPhoto(id_link_1[0]),
        types.InputMediaPhoto(id_link_2[0])] 

        # Отправляем 2 фото и фразу сравнения
        bot.send_media_group(message.chat.id, photos) 
        bot.send_message(message.from_user.id, 
        f"<a href='{id_cleaner(id_link_1[3])}'>{id_link_1[2]}</a> или<a href='{id_cleaner(id_link_2[3])}'>{id_link_2[2]}</a>?", 
        parse_mode='HTML', reply_markup=markup) 

        # Переход к дейсвию после нажатия
        bot.register_next_step_handler(message, on_click_menu)

    elif message.text == '↩️ Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('📊Статистика') 
        btn2 = types.KeyboardButton('🥰Перейти к сравнению') 
        btn3 = types.KeyboardButton('📋Правила') 
        btn4 = types.KeyboardButton('💌Пожелания') 
        markup.add(btn1, btn2, btn3, btn4) # добавить кнопки в меню
        bot.send_message(message.chat.id, "Выберите действие.", reply_markup=markup)
        bot.register_next_step_handler(message, on_click_menu)

@bot.message_handler(commands=['test'])
def test(message):
    global id_link_1
    global id_link_2
    # Задаем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('◀️ Левая') 
    btn2 = types.KeyboardButton('▶️ Правая')
    btn3 = types.KeyboardButton('↩️ Назад')
    markup.add(btn1, btn2, btn3) # добавить кнопки в меню

    # создаем список с types файлов и ссылками на фото
    id_link_1 = get_random_number(message.from_user.id)
    id_link_2 = get_random_number(message.from_user.id)    

    # Составим список из фото
    photos = [types.InputMediaPhoto(id_link_1[0]), types.InputMediaPhoto(id_link_2[0])] 

    # Отправляем 2 фото и фразу сравнения
    bot.send_media_group(message.chat.id, photos) 
    bot.send_message(message.from_user.id, 
    f"<a href='{id_cleaner(id_link_1[3])}'>{id_link_1[2]}</a> или<a href='{id_cleaner(id_link_2[3])}'>{id_link_2[2]}</a>?",
    parse_mode='HTML', reply_markup=markup) 

    # Переход к дейсвию после нажатия
    bot.register_next_step_handler(message, on_click_menu)

# Подключаемся к файлу с данными
df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
df = df[['Link', 'Name', 'Surname', 'Id']]

# Загрузка словаря из файла
try:
    with open('users_state.pickle', 'rb') as users_state_log:
        users_state = pickle.load(users_state_log)
except FileNotFoundError:
    users_state = {}

bot.delete_webhook()
bot.infinity_polling()