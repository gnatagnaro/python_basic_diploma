import telebot
import requests
import config
import webbrowser
import json

API_URL = "https://api.externalwebsite.com/"

bot = telebot.TeleBot(config.token, parse_mode=None)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://google.com/')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Отправьте приветственное сообщение, чтобы получить инструкции по использованию бота. """
    bot.reply_to(message, """\
    Привет, я бот, который может помочь вам найти информацию о externalwebsite.com.
    Пожалуйста, используйте одну из следующих команд:
    /low - приобретайте товары по самой низкой цене
    /high - получить товары по самой высокой цене
    /custom - получить товары в пользовательском ценовом диапазоне
    /history - показать историю вашего недавнего поиска
    /help - получить список команд
    """)

# Define functions for each command


@bot.message_handler(commands=['low'])
def get_lowest_price(message):
    """Получить товары по самой низкой цене из внешнего API"""
    # Спросите пользователя, какой элемент он хочет найти
    bot.reply_to(message, "Какой товар вы хотите найти?")
    bot.register_next_step_handler(message, get_lowest_price_item)


def get_lowest_price_item(message):
    """Получить от пользователя количество элементов для отображения"""
    item = message.text
    bot.reply_to(message, f"Поиск товаров с самой низкой ценой для {item}. Сколько предметов вы хотите увидеть?")
    bot.register_next_step_handler(message, search_lowest_price, item)


def search_lowest_price(message, item):
    """Получить количество элементов для отображения и отправить запрос внешнему API"""
    number_of_items = int(message.text)
    # Создайте URL-адрес запроса API
    url = f"{API_URL}/search?item={item}&order=price&limit={number_of_items}"
    # Запрашивайте API с помощью запросов
    response = requests.get(url)
    # data = json.loads(response.text)
    # Проверка на наличие ошибок
    if response.status_code != 200:
        bot.reply_to(message, "Извините, мы столкнулись с ошибкой при поиске самой низкой цены.")
        return
    # Извлеките результаты из ответа API
    items = response.json()
    # Отображать элементы
    for item in items:
        bot.send_photo(message.chat.id, item['image_url'], caption=f"{item['name']} - {item['price']}")


@bot.message_handler(commands=['high'])
def get_highest_price(message):
    """Получайте товары с самой высокой ценой из внешнего API"""
    # Спросите пользователя, какой элемент он хочет найти
    bot.reply_to(message, "Какой товар вы хотите найти?")
    bot.register_next_step_handler(message, get_highest_price_item)


def get_highest_price_item(message):
    """Получить от пользователя количество элементов для отображения"""
    item = message.text
    bot.reply_to(message, f"Поиск товаров с самой высокой ценой для {item}. Сколько предметов вы хотите увидеть?")
    bot.register_next_step_handler(message, search_highest_price, item)


def search_highest_price(message, item):
    """Получить количество элементов для отображения и отправить запрос внешнему API"""
    number_of_items = int(message.text)
    # Создайте URL-адрес запроса API
    url = f"{API_URL}/search?item={item}&order=price&limit={number_of_items}"
    # Запрашивайте API с помощью запросов
    response = requests.get(url)
    # Проверка на наличие ошибок
    if response.status_code != 200:
        bot.reply_to(message, "Извините, мы столкнулись с ошибкой при поиске самой высокой цены.")
        return
    # Извлеките результаты из ответа API
    items = response.json()
    # Отображать элементы
    for item in items:
        bot.send_photo(message.chat.id, item['image_url'], caption=f"{item['name']} - {item['price']}")


@bot.message_handler(commands=['custom'])
def get_custom_price_range_search(message):
    """Получить товары в пределах пользовательского ценового диапазона из внешнего API"""
    # Спросите пользователя, какой элемент он хочет найти
    bot.reply_to(message, "Какой товар вы хотите найти?")
    bot.register_next_step_handler(message, get_custom_price_range_search_item)


def get_custom_price_range_search_item(message):
    """Получить пользовательский диапазон цен от пользователя"""
    item = message.text
    bot.reply_to(message, f"Поиск {item}. Какой ценовой диапазон вас интересует (например, 10-20)?")
    bot.register_next_step_handler(message, get_custom_price_range_number_of_items, item)


def get_custom_price_range_number_of_items(message, item):
    """Получить от пользователя количество элементов для отображения"""
    price_range = message.text
    price_from, price_to = price_range.split('-')
    bot.reply_to(message, f"Поиск товаров между {price_from} и {price_to} для {item}. "
                          f"Сколько предметов вы хотите увидеть?")
    bot.register_next_step_handler(message, search_custom_price_range, item, price_from, price_to)


def search_custom_price_range(message, item, price_from, price_to):
    """Получить количество элементов для отображения и запросить внешний API"""
    number_of_items = int(message.text)
    # Создайте URL-адрес запроса API
    url = f"{API_URL}/search?item={item}&price_from={price_from}&price_to={price_to}&limit={number_of_items}"
    # Запрашивать API с помощью запросов
    response = requests.get(url)
    # Проверка на наличие ошибок
    if response.status_code != 200:
        bot.reply_to(message, "Извините, мы столкнулись с ошибкой при поиске в пользовательском ценовом диапазоне.")
        return
    # Извлеките результаты из ответа API
    items = response.json()
    # Отобразить элементы
    for item in items:
        bot.send_photo(message.chat.id, item['image_url'], caption=f"{item['name']} - {item['price']}")


@bot.message_handler(commands=['history'])
def show_search_history(message):
    """Показать недавнюю историю поиска пользователя"""
    # TODO: отображение истории последних поисковых запросов
    bot.reply_to(message, "Отображение вашей недавней истории поиска...")


@bot.message_handler()
def hello_world(message):
    """Реакция на команды: 'Привет' и '/hello-world' """
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == '/hello-world':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')


# Запустите бота
bot.polling(none_stop=True)
