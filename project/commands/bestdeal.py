"""
Файл с реализацией команды /bestdeal
"""
from project.search_engine.search_subclass import Searcher
from . import initial_commands as ic
import datetime

from . import search_commands


@ic.mybot.message_handler(commands=['bestdeal'])
def lowprice(message):
	"""Обработка команды bestdeal"""
	search_result = Searcher()
	search_result.search_flag = 2
	cur_time = datetime.datetime.now()
	search_commands.city_querry(message, search_result, cur_time)