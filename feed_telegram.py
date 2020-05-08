#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import hashlib
import logging
from pony.orm import *
import telepot
import tinyurl
import urllib
import time
import requests
import json
from datetime import datetime

LOG_FILENAME = 'riquelme_telegram.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG, format='%(levelname)s:%(message)s')

# DB con Pony

# Riquelme's stuff
control             = 1
filtered_list       = []
container           = []

# twitter
consumer_key        = 'KqKlAMHfLpA9MQzCfRvw'
consumer_secret     = '6lm87f2sE2ncvLLZurGenYha758myCtQAbSE8X8TOQ'
access_token        = '30475748-vUTpUp0yDKu8xFudiv0D5MfyTDARF0C5rHJnJTmpe'
access_token_secret = 'OyZquoi1ipsc2FDQwHPSHBYOYMurBlY6OBwjxnv5M'
auth                = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
url_skynouk         = "https://dev.skynouk.com/api/report_notice"
url_sky_prod        = "https://services.skynouk.com/api/report_notice"
# <functions>


def callParser(call):
  calls_array = call.split()
  pre_content = ""
  if ("INCENDIO" in calls_array[0]):
    title = calls_array[0]
    calls_array.pop(0)
    url   = str(calls_array[-1])
    calls_array.pop(-1)
    machines = calls_array.pop(-1)
    content = calls_array
  else:
    if ("SALE" in calls_array[0]):
      title = calls_array.pop(3)
      url   = calls_array.pop(-1)
      machines = calls_array.pop(1)
      title = "SALE " + str(machines) + " A " + title
      calls_array.pop(0)
      calls_array.pop(0)
      content = calls_array
    else:
      title    = calls_array[0]
      url      = calls_array.pop(-1)
      machines = calls_array.pop(-1)
      calls_array.pop(0)
      content  = calls_array
      if ("10-12" in title):
        title += " " + calls_array.pop(0)
        title += " " + calls_array.pop(0)
  content = ' '.join(content)
  return title, content, machines, url

def get_push_title(text):
  tmp  = text
  text = text.split(' ')
  if("SALE" in tmp):
    r        = text[3] + ' sale ' + text[1] + ' ' + text[-1]
    content  = (((' '.join(text[4:-1])).replace('CALLE ', '')).replace('/', 'y')).replace('AVDA ', '')
    machines = text[1]
    code     = text[3]
  else:
    r        = text[0] + ' sale ' + text[-2] + ' ' + text[-1]
    content  = (((' '.join(text[1:-2])).replace('CALLE ', '')).replace('/', 'y')).replace('AVDA ', '')
    machines = text[-2]
    code     = text[0]
  if text[0] == "INCENDIO":
    r        = text[0] + ' sale ' + text[-1] + ' ' + text[-2]
    content  = (((' '.join(text[1:-2])).replace('CALLE ', '')).replace('/', 'y')).replace('AVDA ', '')
    machines = text[-1]
    code     = text[0]
  return r, content, machines, code

def get_url(text):
  data = text.split(' ')
  return data[-1]


def get_coords(url):
  import urlfetch
  try:
    page = urlfetch.fetch(url)
  except urllib2.URLError, e:
    if e.getcode() == 500:
      content = e.read()
    else:
      raise
  r = urlfetch.get(url, max_redirects=100)
  params = r.history[-1].headers['location']
  params = params.split('q=')
  params = params[1].split('maps?')
  params = params[0].split('&');
  coords = params[0].split(',')
  return coords[0], coords[1]
  params = r.history[-1].headers['location']
  params = params.split('search/')
  params = params[1].split('/data')
  coords = params[0].split(',')
  return coords[0], coords[1]

def check_if_call_exists(call_hash):
  filepath = '/home/kope/dg_general/db1.txt'
  pf   = open(filepath, 'r')
  data = pf.read()
  pf.close()
  data = data.replace("\n", "")
  data = data.split(',')
  if(call_hash in data):
    return False
  else:
    data.append(call_hash)
    buf = ",".join(data)
    pf  = open(filepath, 'w')
    pf.write(buf)
    pf.close()
    return True

def do_query(sql):
  import MySQLdb
  db      = MySQLdb.connect (host = 'localhost', user = 'root', passwd = 'jeveux', db = 'riquelme')
  cursor  = db.cursor()
  cursor.execute(sql)
  last_id = cursor.lastrowid
  result  = cursor.fetchall()
  db.commit()
  cursor.close()
  db.close()
  return result, last_id

def notifyUser(user_id, text):
	sql = "INSERT INTO notifications (not_text, not_user_target) VALUES ('"+ text + "', '"+ user_id +"');"
	do_query(sql)
	return 

def get_id_by_machine_code(mac):
  sql = "SELECT id FROM machine WHERE mac_code = '" + mac + "';"
  result, last_id = do_query(sql)
  return result[0][0]

@db_session
def getTelegramUsersByMachineArray(machine_array):
  hack = False
  db  = Database()
  db.bind('mysql', host='localhost', user='root', passwd='jeveux', db='riquelme')
  sql = "SELECT DISTINCT sub_tg_id FROM subscription WHERE "
  for m in machine_array:
      if hack:
        sql += " OR "
      sql += 'sub_machine_code = "'+m+'" '
      hack = True
  users = db.execute(sql)
  return users
# </functions>


try:
  api                 = tweepy.API(auth)
except:
  pass

try:
  twitters = api.user_timeline(id="CentralCBS")
except:
  twitters = []
for tw in twitters:
  filtered_list.append(tw.text)

for call in filtered_list:
  print call
  m = hashlib.md5()
  m.update(call.encode('utf-8'))
  to_check = m.hexdigest()
  print to_check
  if (check_if_call_exists(to_check)):
    title, content, machines, url = callParser(call)
    lat, lon                       = get_coords(url)
    cHash                          = call[0]

    #payload = {
    #        'key': "1c9e321cb6e3a8210c567f7540e9c6ec",
    #        'title': title,
    #        'content': content,
    #        'location': lat + ',' + lon,
    #        'radio':    2000,
    #        'duration': 60,
    #        'valid_until': "2017-10-09 12:01:02",
    #        'notice_category_id': 4,
    #        'label_provider': "CBS"
	#		}
    url   = "https://dongaby.pompefrance.cl/emergency?"
    url  += "company=4&"
    url  += "lat="     + str(lat)+"&"
    url  += "lon="     + str(lon)+"&"
    url  += "title="   + str(urllib.pathname2url(title.encode('utf-8')))+"&"
    url  += "message=" + str(urllib.pathname2url(content.encode('utf-8')))
    tiny  = tinyurl.create_one(url)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y, %H:%M:%S")
    msg   = str(dt_string) + "\n\n" + title + "\n\n" + content + "\n\n" +  machines + "\n\n" + tiny
    # result, last_id = do_query(sql)
    machines_array  = machines.split(',')
    users           = getTelegramUsersByMachineArray(machines_array)

    for u in users:
      print u
      # notifyUser(u[0], msg)
      # notifyUser(u, msg)

    for u in users:
      logging.debug(str(u) + ": " + str(msg))
      bot = telepot.Bot('138950372:AAE_0yTuQaEIMCiCQOR_YupVTAGCUSTXbvc')
      try: 
          bot.sendMessage(u, msg)
      except telepot.TelegramError:
          pass
      time.sleep(1.5)

