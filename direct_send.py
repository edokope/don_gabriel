#!/usr/bin/python
# -*- coding: utf-8 -*-

import telepot
import emoji

user_id  = 235466532
message  = "Eres una hermosa"

bot      = telepot.Bot('138950372:AAE_0yTuQaEIMCiCQOR_YupVTAGCUSTXbvc')
bot.sendMessage(user_id, emoji.emojize(":thumbsup:", use_aliases=True) + " " + message)

