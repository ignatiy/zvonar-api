#!/bin/bash

if [ -z $1  ]
	then
		echo "Параметр отсутствует или задан неверно!"
		exit 0
else
	curl -s -X POST "https://sms.ru/sms/send?api_id=<ваш ключ>&to=$1&msg=Ваш+текст+сообщения&json=1" > /dev/null
	# любой на выбор или свой	
	curl -s -X POST "https://api.smstraffic.ru/multi.php?login=<логин>&password=<пароль>&phones=$1&message=Ваш+текст+сообщения&rus=5" > /dev/null
	exit 0
fi