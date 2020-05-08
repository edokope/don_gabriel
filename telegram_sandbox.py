#!/usr/bin/python
# -*- coding: utf-8 -*-

import telepot

bot      = telepot.Bot('138950372:AAE_0yTuQaEIMCiCQOR_YupVTAGCUSTXbvc')

counter  = [1,2,3]
offset   = 0

for i in counter:
	try:
		response = bot.getUpdates( offset = offset )
	except telepot.TelegramError as ex:
		reponse = []
		raise

	for msg in response:
		print msg
		offset = msg['update_id'] + 1