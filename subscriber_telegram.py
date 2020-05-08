#!/usr/bin/python
# -*- coding: utf-8 -*-

import telepot
import json
import time
import emoji
import sys
from pony.orm import *
import requests

@db_session
def insert_tg_user(first_name=" ", last_name=" ", tg_id="1"):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	new_id = db.insert("users", usu_firstname=first_name, usu_lastname=last_name, usu_tg_id=tg_id)

@db_session
def exist_tg_user(tg_id):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	user = db.select("* from users where usu_tg_id =$tg_id")
	if len(user) > 0:
		return False
	else:
		return True

@db_session
def check_if_can_subscribe(machine_code, tg_id):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	response = db.select("* from subscription where sub_machine_code = $machine_code and sub_tg_id = $tg_id")
	if len(response) > 0:
		return False
	else:
		return True
@db_session
def subscribe_machine(machine_code, tg_id):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	new_id = db.insert("subscription", sub_machine_code=machine_code, sub_tg_id=tg_id)

@db_session
def check_if_machine_exists(machine_code):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	machine = db.select("* from machine where mac_code = $machine_code ")
	if len(machine) > 0:
		return True
	else:
		return False

@db_session
def unsubscribe_machine(machine_code, tg_id):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	db.execute("DELETE from subscription where sub_machine_code = $machine_code and sub_tg_id = $tg_id")
	
@db_session
def get_subscribed_machines_by_tg_id(tg_id):
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	machines = db.select("sub_machine_code from subscription where sub_tg_id = $tg_id ")
	if len(machines) == 0:
		return "Usted no esta suscrito a ninguna maquina"
	response = "Usted esta siguiendo las siguientes maquinas CBS: "
	for m in machines:
		response += m + " "
	return response

@db_session
def get_availables_machines():
	db = Database()
	db.bind("mysql", host="localhost", user='root', passwd="jeveux", db="riquelme")
	machines = db.select("mac_code FROM machine ORDER BY mac_company_id")
	response = emoji.emojize(":fire_engine:", use_aliases=True) + "\nLista de maquinas disponibles: "
	for m in machines:
		response += m + " "
	return response

debug      = False
offset     = 0
sleep_time = 5

help_text  = """
Uso:
/subscribe <maquina>
Seguir maquina

/unsubscribe <maquina>
Dejar de seguir maquina

/mysubscriptions
Lista de maquinas seguidas

/machineslist
Lista de maquinas disponibles para seguir

/help
Este mensaje de ayuda
    
Pompe France CBS
@edokope
"""

print 'Iniciando Bot Telegram'
print '@cuartabot by kp'

while True:
	time.sleep(sleep_time)
	bot      = telepot.Bot('138950372:AAE_0yTuQaEIMCiCQOR_YupVTAGCUSTXbvc')
	try:
		response = bot.getUpdates(offset=offset)
	except telepot.TelegramError as ex:
		reponse = []
		raise

	for msg in response:
		try:
			if(debug):
				print 'FROM:'
				print json.dumps(msg['message']['from'], ensure_ascii=False)
				print ''
			else:
				print '-------------------'
				print 'From:'
				print msg['message']['from']['first_name'] + ' ' + msg['message']['from']['last_name']
			user_id        = msg['message']['from']['id']
			user_firstname = msg['message']['from']['first_name']
			user_lastname  = msg['message']['from']['last_name']
		except:
			pass
		
		try:
			if(debug):
				print 'CHAT:'
				print json.dumps(msg['message']['chat'], ensure_ascii=False)
				print ''
		except:
			pass
		
		try:
			if(debug):
				print 'MSG: text'
				print json.dumps(msg['message']['text'], ensure_ascii=False)
				print ''
			else:
				print "Msg: "
				print msg['message']['text']
				print '-------------------'
			text = msg['message']['text']
		except:
			pass
		
		try:
			if(debug):
				print 'MSG: id'
				print json.dumps(msg['update_id'], ensure_ascii=False)
				print ''
				print ''
				print '---------------------------------'
			offset = msg['update_id'] + 1
		except:
			pass

		try:
			text_array = text.split(" ")
			if(text_array[0] == "/start"):
				if exist_tg_user(user_id):
					insert_tg_user(user_firstname, user_lastname, user_id)
				bot.sendMessage(user_id, emoji.emojize(":thumbsup:", use_aliases=True) + " Bienvenido/a!\n\nComandos habilitados con /help")
			elif(text_array[0] == "/subscribe"):
				if(check_if_can_subscribe(text_array[1], user_id) and check_if_machine_exists(text_array[1])):
					subscribe_machine(text_array[1], user_id)
					bot.sendMessage(user_id, emoji.emojize(":thumbsup:", use_aliases=True) + " Suscribiendo a  "+ text_array[1])
				else:
					if check_if_can_subscribe(text_array[1], user_id) == False:
						bot.sendMessage(user_id, emoji.emojize(":thumbsdown:", use_aliases=True) + " Ya esta suscrito a "+ text_array[1])
					if check_if_machine_exists(text_array[1]) == False:
						bot.sendMessage(user_id, emoji.emojize(":thumbsdown:", use_aliases=True) + " No se encuentra maquina de nombre " + text_array[1])
			elif(text_array[0] == "/unsubscribe"):
				unsubscribe_machine(text_array[1], user_id)
				bot.sendMessage(user_id, emoji.emojize(":thumbsdown:", use_aliases=True) + " Desuscribiendo a  "+ text_array[1])
			elif(text_array[0] == "/help"):
				bot.sendMessage(user_id, help_text)
			elif(text_array[0] == "/mysubscriptions"):
				bot.sendMessage(user_id, get_subscribed_machines_by_tg_id(user_id))
			elif(text_array[0] == "/machineslist"):
				bot.sendMessage(user_id, get_availables_machines())
			else:
				bot.sendMessage(user_id,emoji.emojize(":shit:", use_aliases=True) + " Comando incorrecto\n\n/help")
		except:
			bot.sendMessage(user_id, emoji.emojize(":shit:", use_aliases=True) + " Error en el comando")

