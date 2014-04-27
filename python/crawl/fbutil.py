import facepy
from fb_keys import FacebookKeys
import re

class FacebookUtil:
	"""
	"""
	
	event_url_pattern = re.compile(r'.*?facebook.com/events/(\d*)(?:/.*?)?')
	access_token = facepy.utils.get_application_access_token(FacebookKeys.app_id, FacebookKeys.app_secret)
	graph = facepy.GraphAPI(access_token)
	
	@staticmethod
	def url_get_event_id(url):
		"""
		This method parses the string pass in through url and
		validates it to make sure it is a proper event URL. If so,
		it parses out the event id
		"""
		result = FacebookUtil.event_url_pattern.search(url)
		if(result == None):
			print("URL: " + url + " is NOT a valid Facebook event")
			return None
			
		event_id = result.group(1)
		
		return event_id
		
	@staticmethod
	def get_event_dict(event_id):
		"""
		Returns the event dictionary that is returned from facepy
		"""
		event = FacebookUtil.graph.get(path=event_id)
		
		return event
