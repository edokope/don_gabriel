#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import hashlib
import string
import base64
import time
import daemon
import logging
import tinyurl
import os 
import urllib


# twitter
consumer_key        = 'KqKlAMHfLpA9MQzCfRvw'
consumer_secret     = '6lm87f2sE2ncvLLZurGenYha758myCtQAbSE8X8TOQ'
access_token        = '30475748-vUTpUp0yDKu8xFudiv0D5MfyTDARF0C5rHJnJTmpe'
access_token_secret = 'OyZquoi1ipsc2FDQwHPSHBYOYMurBlY6OBwjxnv5M'
auth                = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
try:
  api                 = tweepy.API(auth)
except:
  pass

# yowsup
yowsup              = '/home/kope/yowsup/src/yowsup-6345f77b56e474f0eb6143b1363a789254da9ccd/yowsup-cli'
yowsup              = '/home/kope/yowsup/src/yowsup-master/yowsup-cli'

# Parse
parse_app_id        = 'AMrWAAUW99GVRpQLYjQzsITSfVDJNltwq9CPlr0f'
parse_rest_key      = 'HbIi2ite0tuslqyvoZd2vaHDAhdSHfWgGsky7YU1'

# Riquelme
control             = 1
filtered_list       = []
container           = []

# control
debug = True

def log_event(text):
  FORMAT = "%(asctime)s -> %(message)s"
  logging.basicConfig (filename='riquelmeDaemon.log', level=logging.ERROR, format=FORMAT)
  logger = logging.getLogger ('')
  logger.error (text)

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
  params = params.split('search/')
  params = params[1].split('/data')
  coords = params[0].split(',')
  return coords[0], coords[1]

def check_if_call_exists(call_hash):
  filepath = '/home/kope/dg_04ta_CBS/db.txt'
  pf   = open(filepath, 'r')
  data = pf.read()
  pf.close()
  data = data.replace("\n", "")
  data = data.split(',')
  
  if(debug):
    return True
  
  if(call_hash in data):
    return False
  else:
    data.append(call_hash)
    buf = ",".join(data)
    pf  = open(filepath, 'w')
    pf.write(buf)
    pf.close()
    return True

def get_push_title(text):
  tmp  = text
  text = text.split(' ')
  if("SALE" in tmp):
    r       = text[3] + ' sale ' + text[1] + ' ' + text[-1]
    content = (((' '.join(text[4:-1])).replace('CALLE ', '')).replace('/', 'y')).replace('AVDA ', '')
  else:
    r = text[0] + ' sale ' + text[-2] + ' ' + text[-1]
    content = (((' '.join(text[1:-2])).replace('CALLE ', '')).replace('/', 'y')).replace('AVDA ', '')
  return r, content

def get_push_subtitle(text):
  print 'Initial text: ' + text
  text = text.decode('iso-8859-1').encode('utf-8')
  text = text.split(' ')
  print text
  text = text.pop()
  print text
  text = text.pop()
  print text
  text = text.remove(text[0])
  print text
  ret  = ''
  for t in text:
    ret += t
    ret += ' '
  return ret

def add_token(data, call_hash):
  string = ''
  for index in data:
    string = string + ','		

try:
  twitters = api.user_timeline(id="CentralCBS")
except:
  twitters = []
for tw in twitters:
  if ("PRUEBA DE" not in tw.text) & ("0-9" not in tw.text) & ("Informativo" not in tw.text) & ("0-8" not in tw.text) & ("6-8" not in tw.text) & ("En Acto" not in tw.text) & ("PANNE" not in tw.text):
    if (control % 2) != 0:
      m = hashlib.md5()
      m.update(tw.text.encode('utf-8'))
      container.append(m.hexdigest())
      container.append(tw.text)
	
    if (control % 2) == 0:
      container.append(tw.text)
      filtered_list.append(container)
      container = []
    control = control + 1

for call in filtered_list:
  if(('B4' in call[1]) or ('H4' in call[1])) & ('Ubicaci' not in call[1]):
    if (check_if_call_exists(call[0])):
      import json,httplib
      connection = httplib.HTTPSConnection('api.parse.com', 443)
      connection.connect()
      parsed_message, content = get_push_title(call[1])
      connection.request('POST', '/1/push', json.dumps({"where": {"deviceType": "android"},"data": {"alert": content, "title": parsed_message}}), {"X-Parse-Application-Id": "zu7CQv4CsJdrOCvu0aORr259ECvg77HiZlz6oaxx","X-Parse-REST-API-Key": "RrJvY9GRzeysxK8GWMTIF0yERidJ7coZ9cT7jaZ7","Content-Type": "application/json"})
      result = json.loads(connection.getresponse().read())
      lat, lon = get_coords(get_url(call[2]))
      phones = []
      phones.append("56954968988") # kp
      phones.append("56954434267") # Pachita
      phones.append("56993259417") # Monardes
      phones.append("56966686207") # Alejandro Peña
      phones.append("56987217015") # Simon Araya
      phones.append("56957794551") # JP Collao
      phones.append("56984503015") # Manuel Bouyssieres
      phones.append("56992079915") # Andres Campos G
      phones.append("56961491554") # Pablo Pereira
      phones.append("56959002229") # Jean Pierre Chereau
      phones.append("56989230233") # Jose Ahumada
      # phones.append("56985838475") # Pedro Silva
      phones.append("56963009593") # Fernando Ahumada
      phones.append("56990928389") # Sebastian Araya
      phones.append("56942085798") # Gustavo Aravena
      phones.append("56974971178") # Pablo Pignol
      phones.append("56995394190") # Waldo Oiarxun
      phones.append("56962514985") # Miguel Angel Villalon
      phones.append("56957733011") # Gonzalo Aguero
      phones.append("56956938154") # Cesar Carrasco
      phones.append("56993494498") # Pablo Echiburu
      phones.append("56977693599") # Fernando Oyarzo
      phones.append("56966789896") # Waldo Kaltwaser
      phones.append("56976953062") # Nelson Saez
      # phones.append("56974798421") # Michelle Gutierrez
      # phones.append("56985838475-1429563462") # Amigos de la guardia
      # phones.append("56985838475-1446223073") # Guardia
      if (debug):
        phones = []
        phones.append("56954968988") # kp
      new   = "http://dongaby.pompefrance.cl/gabriel/emergency?company=4&lat="+str(lat)+"&lon="+str(lon)+"&title=" + str(urllib.pathname2url(content.encode('utf-8'))) + "&message=" + str(urllib.pathname2url(parsed_message.encode('utf-8')))
      tiny  = tinyurl.create_one(new)
      for phone in phones:
          time.sleep(1)
          cmd   = yowsup + " demos -c /home/kope/yowsup/yowsup-cli.config -s " + phone + " '" + parsed_message + "\n\n" + content + "\n\n" + tiny + "' > /dev/null"
          cmd   = parsed_message + "\n\n" + content + "\n\n" + tiny
          os.system(cmd.encode('utf-8'))
