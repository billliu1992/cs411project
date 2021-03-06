#!venv/bin/python
import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import Queue
import threading

from python.crawl.crawlutil import CrawlUtil
from python.db.common import convert_str_to_datetime
from python.db.eventutil import EventUtil

requests_cache.install_cache()
calendar_links = open("calendar_list.txt")

time_pattern = r'(?P<hour>\d+):(?P<minute>\d+)\s(?P<letter>\w+)'
date_pattern = r'(?P<month>\w+) (?P<day>\d+), (?P<year>\d+)'

t_r = re.compile(time_pattern)
d_r = re.compile(date_pattern)

month_asc = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
		'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
		'Nov': 11, 'Dec':12 }

cal_links_queue = Queue.Queue()
cal_chunks_queue = Queue.Queue()
event_links_queue = Queue.Queue()
event_chunks_queue = Queue.Queue()

class DownloadThread(threading.Thread):
	def __init__(self, queue, out_queue):
		threading.Thread.__init__(self)
		self.queue = queue
		self.out_queue = out_queue

	def run(self):
		while True:
			# grabs host from queue
			link = self.queue.get()

			# grabs urls of hosts and then grabs chunk of webpage
			page_request = requests.get(link)
			page = page_request.text

			# place chunk into out queue
			self.out_queue.put(page)

			# signals to queue job is done
			self.queue.task_done()

class DatamineThread1(threading.Thread):
	def __init__(self, queue, out_queue):
		threading.Thread.__init__(self)
		self.queue = queue
		self.out_queue = out_queue

	def run(self):
		while True:
			# grabs host from queue
			page = self.queue.get()

			# parse the chunk
			page_soup = BeautifulSoup(page, "lxml")
			links = page_soup.find_all(href=re.compile("calendar/detail"))

			for link in links:
				self.out_queue.put(link.get('href'))

			# signals to queue job is done
			self.queue.task_done()

class DatamineThread2(threading.Thread):
	def __init__(self, out_queue):
		threading.Thread.__init__(self)
		self.out_queue = out_queue

	def run(self):
		while True:
			# grabs host from queue
			page = self.out_queue.get()

			# parse the chunk
			soup = BeautifulSoup(page, "lxml")
			description = soup.find("div", class_="description-row")

			if description:
				description = description.get_text()

				if CrawlUtil.is_free_food(description):
					details = soup.find(id="event-wrapper")

					name = details.h2.string
					if name == None:
						continue

					food_obj = CrawlUtil.guess_food_type(description)
					location_obj = "Default location"
					date_str = "Default date"
					time_str = "Default time"

					for child in details.children:
						try:
							key = child.span.string.strip()
							value = child.span.next_sibling.string

							if key == "Location":
								location_obj = CrawlUtil.get_location_or_create(value)
							elif key == "Date":
								date_str = CrawlUtil.parse_date(value, d_r, month_asc)
							elif key == "Time":
								time_str = CrawlUtil.parse_time(value, t_r)

						except AttributeError:
							continue

					if None not in (food_obj, location_obj, date_str, time_str):
						time_obj = convert_str_to_datetime(date_str + ' ' + time_str)

						if CrawlUtil.has_no_duplicate(time_obj,
								location_obj.locationId, food_obj.foodId):
							event = EventUtil.create_event()

							event.time = time_obj
							event.location = location_obj
							event.food = food_obj
							event.name = name

							EventUtil.update_event(event)

							print "created ", name
						else:
							print "found duplicate event ", name

			# signals to queue job is done
			self.out_queue.task_done()

def main():
	# download page containing possible events for the current looked at week
	for i in range(10):
		cal_link2chunk = DownloadThread(cal_links_queue, cal_chunks_queue)
		cal_link2chunk.setDaemon(True)
		cal_link2chunk.start()

	# feed initial download worker threads with links for calendars
	for calendar_link in calendar_links:
		cal_links_queue.put(calendar_link)

	# search for links within the calendar page downloaded
	for i in range(10):
		cal_chunk2event_link = DatamineThread1(cal_chunks_queue, event_links_queue)
		cal_chunk2event_link.setDaemon(True)
		cal_chunk2event_link.start()

	# download event page
	for i in range(10):
		event_link2chunk = DownloadThread(event_links_queue, event_chunks_queue)
		event_link2chunk.setDaemon(True)
		event_link2chunk.start()

	# search description on event's page for mention of food
	for i in range(10):
		event_chunk2parse = DatamineThread2(event_chunks_queue)
		event_chunk2parse.setDaemon(True)
		event_chunk2parse.start()

	cal_links_queue.join()
	cal_chunks_queue.join()
	event_links_queue.join()
	event_chunks_queue.join()

main()
