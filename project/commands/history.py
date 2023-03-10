"""
Файл с реализацией команды /history
"""
from .initial_commands import mybot, users_data


@mybot.message_handler(commands=['history'])
def history_message(message):
    """Обработка команды history"""
    if message.chat.id in users_data:
        mybot.send_message(message.chat.id, 'Вот история вашего поиска')
        for record in users_data[message.chat.id]:
            mybot.send_message(message.chat.id, f'Введенная команда - {record[0]}'
                                                f'\nВремя ввода команды - {record[1]}'
                                                f'\nНайденные отели - {record[2]}')
    else:
        mybot.send_message(message.chat.id, 'Вы еще не делали поисковых запросов')