#!/bin/bash

SRCD='/media/cloud/' #исходная директория
RCVD='/home/autodialer/upload/' #принимающая директория

if [ -z "$(ls -A ${SRCD})" ]; then
	exit 0
else
	rsync -aAv --delete-after --ignore-errors ${SRCD}*.txt ${RCVD}
	rm -f ${SRCD}*.txt
fi
