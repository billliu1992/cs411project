#!venv/bin/python
import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import Queue
import threading

requests_cache.install_cache()

word_list = ['Pizza', 'food', 'drinks', 'Lunch']
calendar_links = open("calendar_list.txt")

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

				for word in word_list:
					if word in description:
						print "found a match in ", description
						details = soup.find(id="event-wrapper")

						for child in details.children:
							try:
								print child.span.string.strip()
								print child.span.next_sibling.string
							except AttributeError:
								continue

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
