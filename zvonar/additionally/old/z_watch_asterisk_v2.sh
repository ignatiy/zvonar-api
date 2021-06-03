#!/bin/bash

SRCD='/media/autodialer/' #исходная директория
RCVD='/etc/asterisk/script/zvonar/' #принимающая директория
LOCK='/media/autodialer/zvonar*.lock' #файл блокировки

if [ -z "$(ls -A ${SRCD})" ]; then # если пусто, то выходим
        exit 0
else
    res=$(ls -A $LOCK | wc -l)
    if [[ "$res" > 0 ]]; then # если есть lock файлы, оповещаем и выходим
        echo "Копирование невозможно! Файл уже занят другой программой"
        exit 0
    else
        find ${SRCD} -type f -not \( -name "IT_diallist.txt" -or -name "DR_diallist.txt" -or -name "diallist.txt" -or -name "test.txt" \) -name "*.txt" -exec cat {} \; > ${SRCD}diallist.txt
        find ${SRCD} -type f -not \( -name "IT_diallist.txt" -or -name "DR_diallist.txt" -or -name "diallist.txt" -or -name "test.txt" \) -name "*.txt" -exec rm -rf {} \;
        mv ${SRCD}*.txt ${RCVD}
        chmod 644 ${RCVD}*.txt
        chown asterisk:asterisk ${RCVD}*.txt

        for file in ${RCVD}*.txt; do # пробегаемся по всем файлам в директории и сравниваем по условию. Исходя из условия выполняем тот скрипт который нужно в фоновом режиме

            filename=$(basename $file)
            result="${filename%.*}"

            if [ $result == 'IT_diallist' ]; then
                nohup ${RCVD}zvonar_it.sh > ${RCVD}zvonar_it.log &
            elif [ $result == 'DR_diallist' ]; then
                nohup ${RCVD}zvonar_dr.sh > ${RCVD}zvonar_dr.log &
            elif [ $result == 'diallist' ]; then
                nohup ${RCVD}zvonar.sh > ${RCVD}zvonar.log &
            elif [ $result == 'test' ]; then
                nohup ${RCVD}test.sh > ${RCVD}zvonar_test.log &
            else
                exit 0
            fi
        done
    fi
fi