#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys

login = "логин"
password = "пароль"
message = "Ваш текст сообщения"

def main(var):
	try:
		url = 'https://api.smstraffic.ru/multi.php'
		obj = {'login': login, 'password': password, 'phones': var, 'message': message, 'rus': 5 }
		response = requests.post(url, data = obj)
		with open("/var/log/zsms.log", "a") as file:
			file.write(response.text)
	except requests.exceptions.ConnectionError:
		print("В соединении отказано")

if __name__ == '__main__':
	if len (sys.argv) > 1:
		main(var=sys.argv[1])
	else:
		print("Параметр отсутствует или задан неверно!")
