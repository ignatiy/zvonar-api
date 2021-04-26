#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config
import sys, traceback
from datetime import datetime
from telegram import Bot, Update, User, Message
from telegram.ext import CommandHandler, Updater, MessageHandler, CallbackContext, Filters
from telegram.utils.request import Request
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def main():
	try:
		request = Request(
			connect_timeout=0.5,
			read_timeout=1.0
		)
		bot = Bot(
			request=request,
			token=config.token,
			base_url=config.proxy #Подготовка прокси на случай блокировки ТГ. в конфиге поменять ссылку на прокси сервер
		)
		updater = Updater(
			bot=bot,
			use_context=True
		)

		response = updater.bot.get_me()
		
		print('*' * 30)
		print('Start telegram: ' + response.username + '\nID: ' + str(response.id) + '')
		print('*' * 30)

		dispatcher = updater.dispatcher
		dispatcher.add_handler(CommandHandler("start", start))
		dispatcher.add_handler(CommandHandler("update", update))
		dispatcher.add_handler(MessageHandler(Filters.text, echoMessage))
		# dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, addNewUserOnChatMember))
		# dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, delUserOnChatMember))
		updater.start_polling()
		updater.idle()
		
		print('\nFinish telegram\n')

	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()