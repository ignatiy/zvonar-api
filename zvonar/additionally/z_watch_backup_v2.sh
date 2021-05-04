#!/bin/bash

SRCD='/media/cloud/' #исходная директория
RCVD='/home/autodialer/upload/' #принимающая директория
SRCD_OLD='/media/cloudmeitan/old/'

if [ -z "$(ls -A ${SRCD})" ]; then
	exit 0
else
	rsync -aAv --delete-after --ignore-errors ${SRCD}*.txt ${RCVD}
	# rm -f ${SRCD}*.txt
	sleep 1
	mv ${SRCD}*.txt ${SRCD_OLD}
fi
