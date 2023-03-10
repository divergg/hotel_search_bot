import dotenv
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class Searcher:
    X_RapidAPI_Key = os.getenv('X-RapidAPI-Key')
    X_RapidAPI_Host = os.getenv('X-RapidAPI-Host')
    content_type = os.getenv('content-type')

    __HEADERS_FOR_LOCATIONS = {
                                "X-RapidAPI-Key": X_RapidAPI_Key,
                                "X-RapidAPI-Host": X_RapidAPI_Host
                                }

    __HEADERS_FOR_SEARCH_QUERY = {
        "content-type": content_type,
        **__HEADERS_FOR_LOCATIONS
    }

    __LINK_TO_LOCATIONS_API = 'https://hotels4.p.rapidapi.com/locations/v3/search'

    __LINK_TO_PROPERTIES_API = 'https://hotels4.p.rapidapi.com/properties/v2/list'

    __LINK_TO_IMAGES_API = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    def __init__(self):
        self._city = ''
        self._regid = ''
        self._distance_from_center = 30
        self._check_in = []
        self._check_out = []
        self._max_nums = 10
        self._hotels = {}
        self._photo_send = False
        self._max_photos = 10
        self._max_price = 150000000
        self._min_price = 1
        self._search_flag = 0
        """self.__serch_flag: 
        0 - используется для команды /lowprice, 1 - используется для команды /highprice, 
        2 - для команды /bestprice"""


    def __get_location_data(self, headers):

        """
        Функция, позволяющая получить из API __LINK_TO_API всю инфу о локациях, подходящих под запрос пользователя
        :param headers: str
        :return: Список информации о локациях (list)
        """
        req = self._city.lower()
        query = {"q": req}
        my_req = requests.get(self.__LINK_TO_LOCATIONS_API , headers=headers, params=query)
        data = json.loads(my_req.text)
        found_list = data['sr']
        return found_list

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, search):
        self._city = search

    def get_possible_locations_list(self):
        found_list = self.__get_location_data(self.__HEADERS_FOR_LOCATIONS)
        names_list = []
        for item in found_list:
            names_list.append(item['regionNames']['fullName'])
        return names_list

    @property
    def regid(self):
        return self._regid

    @regid.setter
    def regid(self, reg_name):
        self._city = reg_name
        found_list = self.__get_location_data(self.__HEADERS_FOR_LOCATIONS)
        self._regid = found_list[0]['gaiaId']


    @property
    def distance_from_center(self):
        return self._distance_from_center

    @distance_from_center.setter
    def distance_from_center(self, value):
        if value < 30:
            self._distance_from_center = value
        else:
            self._distance_from_center = 30

    @property
    def check_in(self):
        return self._check_in

    @check_in.setter
    def check_in(self, date: str):
        self._check_in = date.split()
        if self._check_in[0][0] == '0':
            self._check_in[0] = self._check_in[0][1]
        if self._check_in[1][0] == '0':
            self._check_in[1] = self._check_in[1][1]
        self._check_in = [int(item) for item in self._check_in]


    @property
    def check_out(self):
        return self._check_out

    @check_out.setter
    def check_out(self, date: str):
        self._check_out = date.split()
        if self._check_out[0][0] == '0':
            self._check_out[0] = self._check_out[0][1]
        if self._check_out[1][0] == '0':
            self._check_out[1] = self._check_out[1][1]
        self._check_out = [int(item) for item in self._check_out]

    @property
    def hotels(self):
        return self._hotels

    @property
    def max_nums(self):
        return self._max_nums

    @max_nums.setter
    def max_nums(self, num):
        if num < 10:
            self._max_nums = num
        else:
            self._max_nums = 10

    @property
    def photo_send(self):
        return self._photo_send

    @photo_send.setter
    def photo_send(self, value: bool):
        self._photo_send = value

    @property
    def max_photos(self):
        return self._max_photos

    @max_photos.setter
    def max_photos(self, num):
        if num < 10:
            self._max_photos = num
        else:
            self._max_photos = 10

    @property
    def min_price(self):
        return self._min_price

    @min_price.setter
    def min_price(self, value):
        self._min_price = value

    @property
    def max_price(self):
        return self._max_price

    @max_price.setter
    def max_price(self, value):
        self._max_price = value


    @property
    def search_flag(self):
        return self._search_flag

    @search_flag.setter
    def search_flag(self, value):
        self._search_flag = value


    def post_query(self):
        payload_for_properties_list = {
                    "currency": "USD",
                    "eapid": 1,
                    "locale": "en_US",
                    "siteId": 300000001,
                    "destination": {
                        "regionId": self._regid
                    },
                    "checkInDate": {
                        "day": self._check_in[0],
                        "month": self._check_in[1],
                        "year": self._check_in[2]
                    },
                    "checkOutDate": {
                        "day": self._check_out[0],
                        "month": self._check_out[1],
                        "year": self._check_out[2]
                    },
                    "rooms": [
                        {
                            "adults": 2,
                            "children": []
                        }
                    ],
                    "resultsStartingIndex": 0,
                    "resultsSize": 100,
                    "sort": "PRICE_LOW_TO_HIGH",
                    "filters": {
                        "price": {
                            "max": self._max_price,
                            "min": self._min_price
                        }
                    }
                }
        my_req = requests.post(self.__LINK_TO_PROPERTIES_API, json=payload_for_properties_list, headers=self.__HEADERS_FOR_SEARCH_QUERY)
        data = json.loads(my_req.text)
        self._hotels = {}

        i = 0
        while True:
            if self._search_flag == 0 or self._search_flag == 2:
                index = i
            elif self._search_flag == 1:
                index = -(i+1)
            else:
                raise ValueError
            if data['data']['propertySearch']['properties'][index]['id']:
                if data['data']['propertySearch']['properties'][index]['destinationInfo']['distanceFromDestination']['value'] <= self._distance_from_center:
                    hotel_id = data['data']['propertySearch']['properties'][index]['id']
                    payload_for_images = {
                        "currency": "USD",
                        "eapid": 1,
                        "locale": "en_US",
                        "siteId": 300000001,
                        "propertyId": hotel_id
                    }
                    image_req = requests.post(self.__LINK_TO_IMAGES_API, json=payload_for_images, headers=self.__HEADERS_FOR_SEARCH_QUERY)
                    image_data = json.loads(image_req.text)
                    image_list = [image_data['data']['propertyInfo']['propertyGallery']['images'][j]['image']['url']
                                  for j in range(self._max_photos)]
                    self._hotels.update({data['data']['propertySearch']['properties'][index]['name']:image_list})
                    i += 1
                else:
                    i += 1
                    self._max_nums += 1
                if i == self._max_nums:
                    break
            else:
                break


