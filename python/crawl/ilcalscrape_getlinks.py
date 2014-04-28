#!venv/bin/python
import re
import requests
import requests_cache
from bs4 import BeautifulSoup
from datetime import datetime

requests_cache.install_cache()

today = datetime.today()
today = "%s%02d%02d" % (today.year, today.month, today.day)

f = open("calendar_list.txt", 'w')
r = requests.get("http://illinois.edu/calendar/IllinoisCalendarList")
s = BeautifulSoup(r.text)

for cal_link in s.find_all(href=re.compile("calendar/list")):
	link = cal_link.get('href').split('/')
	url = "http://illinois.edu/calendar/week/" + link[-1:][0] + \
			"?cal=" + today + "&skinId=4" + '\n'
	f.write(url)
