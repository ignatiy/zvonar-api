#!/bin/bash
start=$(date +%s.%N)			# начинаем считать время работы скрипта
count=0					# начальное значение счётчика, пусть он будет в переменной count
pause=180				# пауза между звонками
spooldir=/var/spool/asterisk
diallist=/etc/asterisk/script/zvonar/diallist.txt
lock=/media/autodialer/zvonar.lock

touch $lock				# сделаем файл защиты

echo `date`": Набор номеров с $pause секунд паузой "

while read number; do 			# бесконечный цикл
	((count++))			# увеличиваем счётчик на единицу
	# echo $count			# выводим текущее значение счётчика
	sleep 5

	echo "Channel: Local/8$number@zvonar-dialer
MaxRetries: 1
RetryTime: 5
WaitTime: 25
Context: zvonar-informer
Extension: 999
Callerid: 999
Account: autodialer
Priority: 1" > "$spooldir/tmp/$number"

	chmod 777 $spooldir/tmp/$number
	chown asterisk:asterisk $spooldir/tmp/$number
	mv $spooldir/tmp/$number $spooldir/outgoing

	echo "$number"

	if ! ((count%6)); then		# если значение кратно 6 (остаток от деления равен 0)
		sleep $pause		# то вызываем программу sleep
	fi				# конец условия

done < "$diallist"			# конец цикла

echo "Done"

rm -f $lock				# удаляем файл защиты
rm -f $diallist				# удалим файл с номерами телефонов

end=$(date +%s.%N)			# конец счета времени работы скрипта
result=`echo "$end-$start" | bc -l | xargs printf "%.2f"`	# получаем затраченное время и округляем результат до 2-х знаков после запятой
echo "Время работы: $result секунд"
exit 0					# выходим
