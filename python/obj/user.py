'''
Created on Mar 13, 2014
A class to store the different types of 
users in the system.
@author: Will
'''
class User():

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
	def __init__(self, userId = 0, firstName = "", lastName = "", userName = "", email = "", password = ""):
		self.userId = userId
		self.firstName = firstName
		self.lastName = lastName
		self.userName = userName
		self.email = email
		self.password = password

class EventOrganizer(User):
	def __init__(self):
		pass
