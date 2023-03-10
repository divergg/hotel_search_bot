"""
Файл с реализацией команды /lowprice
"""
from project.search_engine.search_subclass import Searcher
from . import initial_commands as ic
import datetime

from . import search_commands




@ic.mybot.message_handler(commands=['lowprice'])
def lowprice(message):
	"""Обработка команды lowprice"""
	search_result = Searcher()
	search_result.search_flag = 0
	cur_time = datetime.datetime.now()
	search_commands.city_querry(message, search_result, cur_time)





