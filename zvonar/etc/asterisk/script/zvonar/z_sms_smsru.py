#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys

#smsru
api_id = "ключ"
message = "Ваш текст сообщения"

def main(var):
	try:
		url = 'https://sms.ru/sms/send'
		obj = {'api_id': api_id, 'msg': message, 'to': var, 'json': 1 }
		response = requests.post(url, data = obj)
		print(response.text)
		with open("/var/log/zsms.log", "a") as file:
			file.write(response.text)
	except requests.exceptions.ConnectionError:
		print("В соединении отказано")
	

if __name__ == '__main__':
	if len (sys.argv) > 1:
		main(var=sys.argv[1])
	else:
		print("Параметр отсутствует или задан неверно!")