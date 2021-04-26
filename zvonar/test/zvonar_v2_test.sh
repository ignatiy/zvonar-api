#!/bin/bash

start=$(date +%s.%N)			# начинаем считать время работы скрипта
pause=10				# пауза между звонками
count_lines_sip=6			# количество линий в sip
spooldir=/var/spool/asterisk
diallist=/etc/asterisk/script/zvonar/diallist.txt
python_script=/etc/asterisk/script/zvonar
lock=/media/autodialer/zvonar.lock
dircsv=/var/log/asterisk/cdr-csv

touch $lock				# сделаем файл защиты
truncate -s 0 $dircsv/autodialer.csv 			#очистим файл перед началом обзвона

echo `date`": Набор номеров с 5-и секундной паузой"

while read number; do
	sleep 5
	cat <<EOF > $spooldir/tmp/$number
Channel: Local/8$number@zvonar-dialer
MaxRetries: 1
RetryTime: 5
WaitTime: 25
Context: zvonar-informer
Extension: 999
Callerid: 999
Account: autodialer
Priority: 1
EOF
	
	chmod 777 $spooldir/tmp/$number
	chown asterisk:asterisk $spooldir/tmp/$number
	mv $spooldir/tmp/$number $spooldir/outgoing
	
	echo "$number"
	number=`expr $number + 1`

	while [ "$?" -eq "0" ]; do # проверяем значение последней команды
		
		count_files (){
			count_f=`ls $spooldir/outgoing | wc -l`

			if [ "$count_f" -eq "$count_lines_sip" ]; then
				sleep $pause
				return 0
			else
				return 1
			fi
		}

		count_files # запускаем функцию подсчета количества файлов в директории. Если файлов в директории равно количеству линий то засыпаем, иначе дописываем количество до 6-и
	done
done < "$diallist"			# конец цикла

echo "Done"

rm -f $lock				# удаляем файл защиты
rm -f $diallist				# удалим файл с номерами телефонов
cp $dircsv/autodialer.csv $dircsv/autodialer.csv.$(date +%Y-%m-%d-%H-%M).bak			#делаем копию отчета

end=$(date +%s.%N)			# конец счета времени работы скрипта
result=`echo "$end-$start" | bc -l | xargs printf "%.2f"`	# получаем затраченное время и округляем результат до 2-х знаков после запятой
echo "Время работы: $result секунд"
exit 0					# выходим