#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import time
from itertools import groupby
import operator
import collections
from collections import defaultdict

def csv_reader(file_obj):
	reader = csv.reader(file_obj)
	result = []
	data = []
	answered = 0
	noanswer = 0
	busy = 0
	positive_result = 0
	sortedlist = sorted(reader, key=operator.itemgetter(16), reverse=False)
	# print(sortedlist)
	for row in sortedlist:
		rows = dict(uniqueid=(int(float((row[16]))) + int(row[5][6:17])) , callerid=row[1], dcontext=row[2], callid=row[5][6:17], dst=row[7], calltime=row[9], billsec=int(row[12]), disposition=int(row[13]), status=row[14])
		result.append(rows)

	for key, group in groupby(result, key=lambda item: item['uniqueid']):
	    group = list(group)
	    dsts = [item['dst'] for item in group]
	    dcontexts = [item['dcontext'] for item in group]
	    new_item = group[0].copy()
	    if len(dsts) > 1:
	        new_item['dst'] = dsts
	        new_item['dcontext'] = dcontexts
	    # print(new_item)
	    results = 'error'
	    pressed = 'error'
	    callwait = 'error'
	    # print(new_item['status'])
	    # print(new_item['dst'])
	    # print(new_item['dcontext'])

	    if new_item['status'] == 'NO ANSWER' and new_item['dst'] == 'Dial':
	    	# print('Абонент {0} не отвечает. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))#готово
	    	results = '1' #noanswer
	    	pressed = ''
	    	callwait = new_item['billsec']
	    	noanswer += 1
	    if new_item['status'] == 'BUSY' and new_item['dst'] == 'Dial':
	    	# print('Абонент {0} занят или отклонил звонок. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))#готово
	    	results = '2' #busy
	    	pressed = ''
	    	callwait = new_item['billsec']
	    	busy += 1
	    if new_item['status'] == 'ANSWERED':
	    	if new_item['dst'][0] == 'Hangup' and new_item['dcontext'][0] >= '0': #Заменить Hangup на Goto если будем использовать повторное прослушивание
	    		# print('Абонент {0} ответил на звонок. Одно случайное нажатие. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))#готово
	    		results = '0' #answered
	    		pressed = ('{0}'.format(new_item['dcontext'][0]))
	    	
	    	if new_item['dst'][0] == 'Hangup' and new_item['dcontext'][0] == 't': #Заменить Hangup на Goto если будем использовать повторное прослушивание
	    		# print('Абонент {0} ответил на звонок. Нет обратной связи. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))#готово
	    		results = '4' #answered
	    		pressed = ''
	    	
	    	if (new_item['dst'][0] == 'Hangup' and new_item['dcontext'][0] == '1') or (new_item['dst'][0] == 'Hangup' and new_item['dcontext'][0] == '2'):
	    		# print('Абонент {0} ответил на звонок. Положительный результат. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))#готово
	    		results = '0' #answered
	    		pressed = ('{0}'.format(new_item['dcontext'][0]))
	    		positive_result += 1

	    	if new_item['dst'][0] == 'BackGround':
	    		# print('Абонент {0} ответил на звонок. Положил трубку. Дата и время вызова: {1}. Ожидание ответа: {2} секунд. Обработка вызова: {3} секунд.'.format(new_item['callid'], new_item['calltime'], (new_item['billsec'] - new_item['disposition']), new_item['disposition']))
	    		results = '3' #hangup
	    		pressed = ''
	    	if new_item['dst'][0] == 'WaitExten':
	    		results = '4'
	    		pressed = ''
	    	
	    	answered += 1
	    	callwait = new_item['billsec'] - new_item['disposition']
	    
	    data.append((new_item['callid'], results, pressed, new_item['calltime'], callwait, new_item['disposition']))
	
	# print(data)

	A = []
	B = []
	C = []
	S1 = []
	S2 = []
	S3 = []
	S4 = []
	temp_result_data = []
	result_data = []

	for i in data:
		if i[1] == '0' or i[1] == '3' or i[1] == '4':
			A.append(i)
		if i[1] == '1':
			B.append(i)
		if i[1] == '2':
			C.append(i)

	def sub_AC(set_A, set_C):
		Set_out = []
		for x in set_C:
			add = '0'
			for i in set_A:
				if x[0] == i[0]:
					add = '1'
					break
			if add =='0':
				Set_out.append(x)
		return Set_out

	S1 = sub_AC(A, C)

	def sub_AB(set_A, set_B):
		Set_out = []
		for x in set_B:
			add = '0'
			for i in set_A:
				if x[0] == i[0]:
					add = '1'
					break
			if add =='0':
				Set_out.append(x)
		return Set_out

	S2 = sub_AB(A, B)

	def sub_S2C(set_S2, set_C):
		Set_out = []
		for x in set_S2:
			add = '0'
			for i in set_C:
				if x[0] == i[0]:
					add = '1'
					break
			if add =='0':
				Set_out.append(x)
		return Set_out

	S4 = sub_S2C(S2, C)

	def sub_S1S4(set_S1, set_S4):
		Set_out = []
		for x in set_S1:
			add = '0'
			for i in set_S4:
				if x[0] == i[0]:
					add = '1'
					break
			if add =='0':
				Set_out.append(x)
		return Set_out

	S3 = sub_S1S4(S1, S4)

	for x in A:
		temp_result_data.append(x)
	for x in S3:
		temp_result_data.append(x)
	for x in S4:
		temp_result_data.append(x)

	d = defaultdict(list)
	for p1,p2,p3,p4,p5,p6 in temp_result_data:
		d[p1].append((p1,p2,p3,p4,p5,p6))

	for x in d:
		result_data.append(d[x][0])	
	
	# print(temp_result_data)
	csv_writer(data=result_data)

	# для телеги
	print('-' * 50)
	print('Неотвечено {0}'.format(noanswer))
	print('Занято {0}'.format(busy))
	print('Отвечено {0}'.format(answered))
	print('Положительных результатов {0}'.format(positive_result))

def csv_writer(data):
	with open("/home/sysadmin2/Рабочий стол/report.csv", "w") as csv_file: # открываем файл на запись
		writer = csv.writer(csv_file, delimiter=';') # добавляем разделитель
		for line in data:
			writer.writerow(line) # заполняем файл полученными данными
	with open("/home/sysadmin2/Рабочий стол/report.csv", "w") as csv_file: # снова открываем файл на запись
		writer = csv.writer(csv_file, delimiter=';') # добавляем разделитель
		writer.writerow(['Номер', 'Статус звонка (Отвечено: 0 / Не отвечено: 1 / Занято: 2 / Сбросили: 3 / Отвечено но ничего не выбрано: 4)', 'Выбрано', 'Дата и время звонка', 'Ожидание ответа в сек.', 'Обработка вызова в сек.']) # и добавляем заголовки
		writer.writerows(data)

if __name__ == '__main__':
	csv_path = "/home/sysadmin2/Рабочий стол/autodialer.csv"
	with open(csv_path, "r") as f_obj:
		csv_reader(f_obj)


