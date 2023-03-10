from . import initial_commands as ic
from telebot import types
import time





def city_querry(message, search_result, cur_time):
	"""Запрос названия города у пользователя и сохранение его в экземпляре класса"""
	request = message
	def get_city():
		reply = ic.mybot.send_message(message.chat.id,
									  'Введите название города, в котором будет проводиться поиск отелей')
		ic.mybot.register_next_step_handler(reply, set_city)

	def set_city(inp):
		search_result.city = inp.text
		menu(message, search_result, cur_time, request)

	get_city()



def menu(message, search_result, cur_time, request):

	def correct_city():
		"""Меню для уточнения выбора города """
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
		for item in search_result.get_possible_locations_list():
			markup.add(item)
		reply = ic.mybot.send_message(message.chat.id, 'Уточните название города из списка ниже', reply_markup=markup)
		ic.mybot.register_next_step_handler(reply, check_in_date)

	def check_in_date(inp):
		"""Ввод даты заезда-"""
		search_result.regid = inp.text
		reply = ic.mybot.send_message(inp.chat.id, 'Введите дату заезда (в формате ДД ММ ГГГГ)',
									  reply_markup=types.ReplyKeyboardRemove())
		ic.mybot.register_next_step_handler(reply, check_out_date)

	def check_out_date(inp):
		"""Ввод даты выезда"""
		search_result.check_in = inp.text
		reply = ic.mybot.send_message(inp.chat.id, 'Введите дату выезда (в формате ДД ММ ГГГГ)')
		ic.mybot.register_next_step_handler(reply, set_check_out_date)

	def set_check_out_date(inp):
		"""Сохранение даты заезда в классе поиска"""
		search_result.check_out = inp.text
		if search_result.search_flag == 2:
			maximum_price(inp)
		else:
			set_maximum_hotels(inp)

	def maximum_price(inp):
		"""Установление максимальной цены за ночь"""
		reply = ic.mybot.send_message(inp.chat.id, 'Введите максимальную цену за ночь')
		ic.mybot.register_next_step_handler(reply, set_max_price)

	def set_max_price(inp):
		"""Сохранение максимальной цены в классе поиска и запрос на ввод минимальной цены"""
		search_result.max_price = int(inp.text)
		reply = ic.mybot.send_message(inp.chat.id, 'Введите минимальную цену за ночь')
		ic.mybot.register_next_step_handler(reply, set_min_price)

	def set_min_price(inp):
		"""Сохранение минимальной цены и запрос на ввод расстояния"""
		search_result.min_price = int(inp.text)
		reply = ic.mybot.send_message(inp.chat.id, 'Введите максимальное расстояние до центра (не более 30 миль)')
		ic.mybot.register_next_step_handler(reply, set_dist)


	def set_dist(inp):
		"""Сохранение расстояния в классе поиска"""
		search_result.distance_from_center = float(inp.text)
		set_maximum_hotels(inp)

	def set_maximum_hotels(inp):
		"""Установление максимального количества отелей"""
		reply = ic.mybot.send_message(inp.chat.id, 'Введите максимальное количество выводимых отелей (не более 10)')
		ic.mybot.register_next_step_handler(reply, check_input_number)

	def check_input_number(inp):
		"""Проверка правильности введенного числа отелей"""
		if inp.text.isdigit():
			get_photos(inp)
		else:
			set_maximum_hotels(ic.mybot.send_message(inp.chat.id, 'Неправильный ввод'))

	def get_photos(inp):
		"""Запрос на вывод изображений отеля"""
		search_result.max_nums = int(inp.text)
		reply = ic.mybot.send_message(inp.chat.id, 'Требуется вывод фото? (да/нет)')
		ic.mybot.register_next_step_handler(reply, check_photo_input)

	def check_photo_input(inp):
		"""Установка флажка для вывода фото и получение количества выводимых фото"""
		if inp.text.lower() == 'да':
			search_result.photo_send = True
			reply = ic.mybot.send_message(inp.chat.id, 'Введите количество выводимых фото (не более 10)')
			ic.mybot.register_next_step_handler(reply, set_maximum_photos)

		else:
			search_result.photo_send = False
			send_hotel_info(inp)

	def set_maximum_photos(inp):
		"""Проверка ввода количества фото"""
		if inp.text.isdigit():
			search_result.max_photos = int(inp.text)
			send_hotel_info(inp)
		else:
			set_maximum_photos(ic.mybot.send_message(inp.chat.id, 'Неправильный ввод'))

	def send_hotel_info(inp):
		"""Финальный вывод информации"""
		search_result.post_query()
		if search_result.photo_send:
			for item in search_result.hotels:
				ic.mybot.send_message(inp.chat.id, item)
				time.sleep(1)
				for img in search_result.hotels[item]:
					ic.mybot.send_message(inp.chat.id, img)
					time.sleep(1)
		else:
			for item in search_result.hotels:
				ic.mybot.send_message(inp.chat.id, item)
				time.sleep(1)
		ic.logging(request, cur_time.strftime("%d/%m/%Y %H:%M:%S"), ', '.join(search_result.hotels.keys()))

	correct_city()















