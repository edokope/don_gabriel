#!/usr/bin/python
# -*- coding: utf-8 -*-

import telepot
import emoji

user_id  = 1080516
message  = "Quiero esa moto"

token    = "363839141:AAFqbMH84iZJuTjdSJot5ZJ-IuKJVIEcFCo"

bot      = telepot.Bot(token)
try:
	bot.sendMessage(user_id, emoji.emojize(":thumbsup:", use_aliases=True) + " " + message)
except telepot.TelegramError:
	print "cago"
	pass
	# print telepot.TelegramError.description

