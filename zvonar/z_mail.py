#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import path
import datetime
import shutil

sys.path.insert(0, '../')

def sendmail(var):
	try:
		path = '/etc/asterisk/script/zvonar/report.csv'
		if os.path.exists(path):
			if os.path.getsize(path) > 0:
				# for To in ["email1"]: # проходим циклом по списку тех, кому нужно отправить письма  
				From = "здесь" # задаем адрес отправителя
				Pass = "пароль" # задаем пароль
				msg = MIMEMultipart() # создаем объект сообщение
				msg['From'] = From
				msg['To'] = var
				msg['Subject'] = 'Отчет autodialer'
				body = "Во вложении файл отчета автопрозвона\nРазделитель - ;\n\n{}\nЭто письмо создано автоматически, отвечать на него не нужно!".format('-' * 60)
				msg.attach(MIMEText(body, 'plain')) # добавляем наши заголовки в сообщении
				with open(path, 'rb') as fp: # открываем наш файл на чтение
					file = MIMEBase('text', 'plain') # объявляем нашему файлу типы (текстовый и простой)
					file.set_payload(fp.read()) # создаем полезную нагрузку на чтение файла
					encoders.encode_base64(file) # кодируем в base64
					timer = datetime.datetime.now()
					file.add_header('Content-Disposition', 'attachment', filename='report_{}.csv'.format(timer.strftime('%Y-%m-%d'))) # добавляем заголовки файлу
					msg.attach(file) # прикрепляем к сообщению
					fp.close() # закрываем файл
				server = smtplib.SMTP('ip адрес сервера', 25) # создаем объект для работы с протоколом SMTP и указываем с какого сервера отправлять и порт
				server.set_debuglevel(False) # режим отладки. True включает отладку. Полезно почитать вывод smtplib
				server.starttls() # создаем шифрованное сообщение TLS
				server.login(From, Pass) # логинимся
				server.send_message(msg) # отправляем сообщение
				server.quit() # закрываем соедение
				print("Письмо успешно отправлено")
			else:
				print("Файл пуст")
		else:
			print("Файл отсутствует")
	
	except:
		print("Произошла ошибка при отправке письма.")
	finally:
		pass

if __name__ == '__main__':
	if len(sys.argv) > 1:
		sendmail(var=sys.argv[1])
	else:
		print("Укажите Email адрес!")
