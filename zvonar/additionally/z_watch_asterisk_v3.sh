#!/bin/bash

SRCD='/media/sysadmin2/Data/Project/zvonar-api/zvonar/additionally/test/' #исходная директория
RCVD='/media/sysadmin2/Data/Project/zvonar-api/zvonar/additionally/tests/' #принимающая директория
LOCK='/media/sysadmin2/Data/Project/zvonar-api/zvonar/additionally/test/zvonar*.lock' #файл блокировки
SRCD_OLD='/media/sysadmin2/Data/Project/zvonar-api/zvonar/additionally/test/old/' #старые файлы

result_test=`ls -A ${SRCD}test*.txt | wc -l`
result_it=`ls -A ${SRCD}IT_diallist*.txt | wc -l`
result_dr=`ls -A ${SRCD}DR_diallist*.txt | wc -l`

if [ -z "$(ls -A ${SRCD})" ]; then # если пусто, то выходим
	exit 0
else
	res=$(ls -A $LOCK | wc -l)
	if [[ "$res" > 0 ]]; then # если есть lock файлы, оповещаем и выходим
        echo "Копирование невозможно! Файл уже занят другой программой"
        exit 0
    else
    	if [[ "$result_test" > 0 ]]; then
			sort ${SRCD}test*.txt | awk '!seen[$0]++' ${SRCD}test*.txt > ${RCVD}test.txt
			sleep 1
			mv ${SRCD}test*.txt $SRCD_OLD
		else
			echo "Файл test не существуют"
		fi

		if [[ "$result_it" > 0 ]]; then
			sort ${SRCD}IT_diallist*.txt | awk '!seen[$0]++' ${SRCD}IT_diallist*.txt > ${RCVD}IT_diallist.txt
			sleep 1
			mv ${SRCD}IT_diallist*.txt $SRCD_OLD
		else
			echo "Файл IT_diallist не существуют"
		fi

		if [[ "$result_dr" > 0 ]]; then
			sort ${SRCD}DR_diallist*.txt | awk '!seen[$0]++' ${SRCD}DR_diallist*.txt > ${RCVD}DR_diallist.txt
			sleep 1
			mv ${SRCD}DR_diallist*.txt $SRCD_OLD
		else
			echo "Файлы DR_diallist не существуют"
		fi

		chmod 644 ${RCVD}*.txt
		chown asterisk:asterisk ${RCVD}*.txt

  		# find ${SRCD} -type f -not \( -name "IT_diallist.txt" -or -name "DR_diallist.txt" -or -name "diallist.txt" \) -name "*.txt" -exec cat {} \; > ${SRCD}diallist.txt
		# find ${SRCD} -type f -not \( -name "IT_diallist.txt" -or -name "DR_diallist.txt" -or -name "diallist.txt" \) -name "*.txt" -exec rm -rf {} \;
		for file in ${RCVD}*.txt; do # пробегаемся по всем файлам в директории и сравниваем по условию. Исходя из условия выполняем тот скрипт который нужно в фоновом режиме
                        
			filename=$(basename $file)
			result="${filename%.*}"
			
			if [ $result == 'IT_diallist' ]; then
				nohup ${RCVD}zvonar_it.sh > ${RCVD}zvonar_it.log &
			elif [ $result == 'DR_diallist' ]; then
				nohup ${RCVD}zvonar_dr.sh > ${RCVD}zvonar_dr.log &
			elif [ $result == 'test' ]; then
				nohup ${RCVD}zvonar-test.sh > ${RCVD}zvonar-test.log &
			else
			    exit 0
			fi
        done

    fi
fi
