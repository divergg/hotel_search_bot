import telebot
from dotenv import load_dotenv
import os



load_dotenv()
TOKEN = os.getenv('TOKEN')
mybot = telebot.TeleBot(TOKEN)
users_data = {}



def logging(message, time, record):
    """Функция, осуществляющая запись поисков пользователя в словарь"""
    if message.chat.id in users_data:
        users_data[message.chat.id].append((message.text, time, record,))
    else:
        users_data.update({message.chat.id: [(message.text, time, record,)]})


@mybot.message_handler(commands=['start'])
def start_message(message):
    """Обработка команды старт"""
    mybot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '\nИспользуйте команду /help для получения помощи.')


@mybot.message_handler(commands=['help'])
def help_message(message):
    """Обработка команды help"""
    mybot.send_message(message.chat.id,
                       'В настоящее время бот находится в разработке. Перечень доступных комманд:'
                       '\n/help - вызов справки'
                       '\n/lowprice - получение отелей, отсортированных по возрастанию цены'
                       '\n/highprice - получение отелей, отсортированных по убыванию цены'
                       '\n/bestdeal - получение отелей в заданном диапазоне цен и на заданном расстоянии от центра города'
                       '\n/history - история вашего поиска')



@mybot.message_handler(commands=['helloworld'])
def hello_world(message):
    """Обработка команды helloworld"""
    mybot.send_message(message.chat.id, 'Мир прекрасен!')


@mybot.message_handler(regexp='привет')
def hello(message):
    """Ответ на запрос "Привет"""
    mybot.send_message(message.chat.id, 'И вам привет!')




