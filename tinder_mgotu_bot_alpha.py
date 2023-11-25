import telebot
from telebot import types
import pandas as pd 
import random2 as random
import pickle

bot = telebot.TeleBot('6719752669:AAEaWTGqzEUS8iJbrX0EZZWhDSDg-nyMmng')

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

def making_rating(df_rating, a, b, inpt):
    # Найти элементы в списке по их id и посчитать их E
    element_a = df_rating.iloc[a].to_list()
    element_b = df_rating.iloc[b].to_list()
    # Это должно происходить внутри фунцкии get_random_num
    R_a = float(element_a[2])
    R_b = float(element_b[2])
    # Если два элемента еще не сравнивались им присваевается 1000 баллов Elo
    if R_a == float(0.0) and R_b == float(0.0):
        R_a += 1000.0
        R_b += 1000.0
    elif R_a == 0:
        R_a += 1000.0
    elif R_b == 0:
        R_b += 1000.0
    # Нахождение предположительного рейтинга Elo
    E_a = 1/(1 + (10**((R_b - R_a)/480)))
    E_b = 1/(1 + (10**((R_a - R_b)/480)))
    # Ранжировка коэф-та в зависимости от рейтинга
    if R_a < 2100.0:
        k_a = 32
    elif 2100.0 <= R_a <= 2400.0:
        k_a = 24
    elif  k_a > 2400.0:
        k_a = 16
    if R_b < 2100.0:
        k_b = 32
    elif 2100.0 <= R_b <= 2400.0:
        k_b = 24
    elif  k_b > 2400.0:
        k_b = 16

    if "◀️ Левая" == inpt:
        # Calculate Elo if 1 wins
        df_rating.at[a, 'Elo'] = R_a + k_a*(1-E_a)
        df_rating.at[b, 'Elo'] = R_b + k_b*(0-E_b)
        # Increment counter
        df_rating.at[a, 'Count'] += 1
        df_rating.at[b, 'Count'] += 1
        # writing in file
        df_rating.to_csv('./bio_rating.txt', header=False, index=False)
    elif "▶️ Правая" == inpt:
        # Calculate elo if 2 wins
        df_rating.at[b, 'Elo'] = R_b + k_b*(1-E_b)
        df_rating.at[a, 'Elo'] = R_a + k_a*(0-E_a)
        # Increment counter
        df_rating.at[a, 'Count'] += 1
        df_rating.at[b, 'Count'] += 1
        # writing in file
        df_rating.to_csv('./bio_rating.txt', header=False, index=False)
    

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
        rating_list = df_rating.sort_values(by='Elo', ascending=False)[df_rating['Count'] != 0.0]['FIO'].head(10).to_list()
        rating_list = '\n'.join([f"{index + 1}. {line}" for index, line in enumerate(rating_list)])
        # print(df_rating.sort_values(by='Elo', ascending=False)[df_rating['Count'] != 0.0]['FIO'].head(10).to_list())
        # bot.send_message(message.chat.id, f'1.{rating_list[1-1]}\n2.{rating_list[2-1]}\n3.{rating_list[3-1]}\n4.{rating_list[4-1]}\n5.{rating_list[5-1]}\n6.{rating_list[6-1]}\n7.{rating_list[7-1]}\n8.{rating_list[8-1]}\n9.{rating_list[9-1]}\n10.{rating_list[10-1]}\n', reply_markup=markup) 
        bot.send_message(message.chat.id, 'Топ 10 красавиц нашего университета', reply_markup=markup)
        bot.send_message(message.chat.id, f'{rating_list}')
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
        a = df[df['Id'] == id_link_1[3]].index[0]
        b = df[df['Id'] == id_link_2[3]].index[0]
        making_rating(df_rating, a, b, '◀️ Левая')
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
        a = df[df['Id'] == id_link_1[3]].index[0]
        b = df[df['Id'] == id_link_2[3]].index[0]
        making_rating(df_rating, a, b, '▶️ Правая')
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

# Подключаемся к файлу с данными о девушках
df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
df = df[['Link', 'Name', 'Surname', 'Id']]
# Подключаемся к файлу с данными о рейтинге девушек
df_rating = pd.read_csv('./bio_rating.txt', encoding='utf-8', header=None)
df_rating.columns = ['FIO', 'Count', 'Elo']


# Загрузка словаря из файла
try:
    with open('users_state.pickle', 'rb') as users_state_log:
        users_state = pickle.load(users_state_log)
except FileNotFoundError:
    users_state = {}

bot.delete_webhook()
bot.infinity_polling()
