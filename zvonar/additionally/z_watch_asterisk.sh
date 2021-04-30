#!/bin/bash

SRCD='/media/autodialer/' #исходная директория
RCVD='/etc/asterisk/script/zvonar/' #принимающая директория
LOCK='/media/autodialer/zvonar.lock' #файл блокировки

if [ -z "$(ls -A ${SRCD})" ]; then # если пусто, то выходим
        exit 0
else # инчае проверяем lock файл
        if [[ -f $LOCK ]]; then # если есть lock файл, оповещаем и выходим
                echo "Копирование невозможно! Файл уже занят другой программой"
                exit 0
        else # если нет то копируем файлы и запускаем работу zvonar, предварительно назначив разрешения всем txt файлам
                rsync -aAv --delete-after --ignore-errors ${SRCD}*.txt ${RCVD}                
                rm -f ${SRCD}*.txt
                chmod 644 ${RCVD}*.txt
                chown asterisk:asterisk ${RCVD}*.txt
                
                for file in ${RCVD}*.txt; do # пробегаемся по всем файлам в директории и сравниваем по условию. Исходя из условия выполняем тот скрипт который нужно в фоновом режиме
                        
                        filename=$(basename $file)
                        result="${filename%.*}"

                        #sort test*.txt | awk '!seen[$0]++' test*.txt > test.txt
                        #вкрутить вот сюда

                        if [ $result == 'IT_diallist' ]; then
                                nohup ${RCVD}zvonar_it.sh > ${RCVD}zvonar.log &
                        elif [ $result == 'DR_diallist' ]; then
                                nohup ${RCVD}zvonar_dr.sh > ${RCVD}zvonar.log &
			elif [ $result == 'diallist' ]; then
				nohup ${RCVD}zvonar_v2.sh > ${RCVD}zvonar.log &
                        else
                                exit 0
                        fi
                done
        fi
fi
