#!/bin/bash

SRCD='/media/cloud/' #исходная директория
RCVD='/home/autodialer/upload/' #принимающая директория
SRCD_OLD='/media/cloud/old/' #старые файлы

result_test=`ls -A ${SRCD}test*.txt | wc -l`
result_it=`ls -A ${SRCD}IT_diallist*.txt | wc -l`
result_dr=`ls -A ${SRCD}DR_diallist*.txt | wc -l`

if [ -z "$(ls -A ${SRCD})" ]; then
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
		# rm -f ${SRCD}IT_diallist*.txt
		mv ${SRCD}IT_diallist*.txt $SRCD_OLD
	else
		echo "Файл IT_diallist не существуют"
	fi

	if [[ "$result_dr" > 0 ]]; then
		sort ${SRCD}DR_diallist*.txt | awk '!seen[$0]++' ${SRCD}DR_diallist*.txt > ${RCVD}DR_diallist.txt
		sleep 1
		# rm -f ${SRCD}DR_diallist*.txt
		mv ${SRCD}DR_diallist*.txt $SRCD_OLD
	else
		echo "Файлы DR_diallist не существуют"
	fi
fi
