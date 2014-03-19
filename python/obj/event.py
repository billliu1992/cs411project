'''
Created on Mar 13, 2014
A class to store the free food event data.
@author: Will
'''
class Event():
	'''
	Initializes the event with
	the given information 
	The formatting of each is left
	as a decision for the user.
	@param name the name of the event
	@param time the time of the event
	@param location an instance of a Location object
	@param food an instance of a Food object
	'''
	def __init__(self,eventid = 0, name = "", time = None, location = None, food = None, organizer = None):
		self.name = name
		self.time = time 
		self.location = location
		self.food = food
		self.organizer = organizer
		self.eventId = eventid
	
