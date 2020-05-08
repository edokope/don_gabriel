
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

calls = [
"10-12 A 2da CALLE LO ECHEVERS / AVDA CAMINO LO-ECHEVERS B21 https://t.co/bor4hdbSJu", 
"10-3-4 CALLE ARTURO PRAT / CALLE ELEUTERIO RAMIREZ M8,RX6 https://t.co/bor4hdbSJu",
"SALE X3 A INCENDIO AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE https://t.co/bor4hdbSJu",
"SALE S2 A INCENDIO AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE https://t.co/bor4hdbSJu",
"SALE K3 A INCENDIO AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE https://t.co/bor4hdbSJu",
"SALE K1 A INCENDIO AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE https://t.co/bor4hdbSJu",
"INCENDIO AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE  B13, B14, B18, B19, B20, BM20, BT3, H4, M2-N, Q15, Q8, RX15 https://t.co/bor4hdbSJu",
"10-0-2 AVDA PRESIDENTE KENNEDY / AVDA MANQUEHUE NORTE B18,B20,Q15,BM20,M2-N https://t.co/bor4hdbSJu",
"10-0-2 CALLE CABO DE HORNO / CALLE GENERAL FREIRE B21,BX7QN,Q8,B22,M6QN https://t.co/bor4hdbSJu"]

print ""

for call in calls:
  print ""
  call = call.replace(", ", ",")
  title, content, machines, url = callParser(call)
  lat, lon = get_coords(url)
  print "TITLE    : " + title
  print "CONTENT  : " + content
  print "machines : " + machines
  print "url      : " + url
  print "lat      : " + lat
  print "lon      : " + lon

print ""
