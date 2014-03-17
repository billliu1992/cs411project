'''
Created on Mar 13, 2014
A class to store the different types of 
users in the system.
@author: Will
'''
class User():
	global first_name
	global last_name
	global user_name
	global email
	global liked_food
	global prefd_location

	'''
	Initializes the user with
	the given information.
	@param first_name the user's first name
 	@param last_name the user's last name
	@param user_name the user's username
	@param email the user's email address
	@param liked_food an array of foods the user likes
	@param prefd_location an array of places the user prefers
	'''
	def set_info(self,first_name,last_name,email,liked_food,prefd_location):
		self.first_name = first_name
		self.last_name = last_name
		self.user_name = user_name
		self.email = email
		self.liked_food = liked_food
		self.pred_location = prefd_location

class EventOrganizer(User):
	global events
