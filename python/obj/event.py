'''
Created on Mar 13, 2014
A class to store the free food event data.
@author: Will
'''
class Event():
	global name
	global time
	global location
	global food
	
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
	def set_info(self,name,time,location,food):
		self.name = name
		self.time = time 
		self.location = location
		self.food = food

	def get_name(self):
		return self.name
	
	def get_time(self):
		return self.time
	
