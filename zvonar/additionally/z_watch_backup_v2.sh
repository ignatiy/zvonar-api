#!/bin/bash

SRCD='/media/cloudmeitan/' #исходная директория
RCVD='/home/autodialer/upload/' #принимающая директория
LOCK='/home/autodialer/upload/zvonar*.lock'

if [ -z "$(ls -A ${SRCD})" ]; then
	exit 0
else
	res=$(ls -A $LOCK | wc -l)
	if [[ "$res" > 0 ]]; then # если есть lock файлы, выходим
        echo "Копирование невозможно! Файл уже занят другой программой"
        exit 0
    else
    	mv ${SRCD}*.txt ${RCVD}
    fi
fi
