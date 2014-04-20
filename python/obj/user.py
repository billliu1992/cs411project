'''
Created on Mar 13, 2014
A class to store the different types of 
users in the system.
@author: Will
'''
from python.db.common import *

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
	def __init__(self, userId = 0, firstName = "", lastName = "", userName = "", email = "", password = "", authenticated =""):
		self.userId = userId
		self.firstName = firstName
		self.lastName = lastName
		self.userName = userName
		self.email = email
		self.password = password
		self.authenticated = authenticated
		self.location_pref = []
		self.food_pref = []

	def get_id(self):
		return self.userName

	def is_authenticated(self):
		return self.authenticated

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	@staticmethod
	def get(username):
		connection = connect_to_db()
		cursor = connection.cursor()

		cursor.execute("""
		SELECT * FROM User WHERE userName=%s;
		""", (username,))

		user=cursor.fetchone()
		connection.close()

		if user:
			return User(user[0], user[1], user[2], user[3], user[4],
					user[5], user[6])
		else:
			return None

	def authenticate(self, auth=True):
		connection = connect_to_db()
		cursor = connection.cursor()

		cursor.execute("""
		UPDATE User
		SET authenticated=%s
		WHERE userId=%s;
		""", (int(auth), self.userId))

		connection.commit()
		connection.close()

"""
class EventOrganizer(User):
	def __init__(self):
		pass
"""
