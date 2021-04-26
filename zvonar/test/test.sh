#!/bin/bash
COMMAND=`/bin/systemctl status asterisk | grep Active | sed -r 's/.*\((.*)\).*/\1/'`

if [[ "$COMMAND" == "dead" ]]; then
	echo "Не работает"
elif [[ "$COMMAND" == "running" ]]; then
	echo "Работает"
fi