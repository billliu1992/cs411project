from common import *
from python.obj.user import User
import datetime

class UserUtil:
	@staticmethod
	def create_user():
		"""
		Creates an user in the database, and returns an object for the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			INSERT INTO User (firstName, lastName, userName, email, password)
			VALUES ("", "", "", "", "");
			""")
			
		connection.commit()
		return User(connection.insert_id())
		
	@staticmethod
	def update_user(user_obj):
		"""
		Updates the user in the database only if the user exists
		"""
		if(not isinstance(user_obj, User)):
			print("Passed in wrong object when updating user")
		
		connection = connect_to_db()
		cursor = connection.cursor()
		
		
		result = cursor.execute("""
			UPDATE User SET
			firstName = %s
			lastName  = %s
			userName  = %s
			email  = %s
			password  = %s
			WHERE
			userId = %s;
			""", (user_obj.firstName, user_obj.lastName, user_obj.userName, user_obj.email, user_obj.password, user_obj.userId))
		
		connection.commit()
		connection.close()
		
	@staticmethod
	def get_user(userId):
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM User WHERE
			userId = %s
			""", (userId,))
		
		result = cursor.fetchall()
		
		if(len(result) > 0):
			return UserUtil.convert_array_to_obj(result[0])
		else:
			print("User: " + str(userId) + " does not exist")
			return None
			
	@staticmethod
	def convert_array_to_obj(array):
		userId, firstName, lastName, userName, email, password = array
		return User(userId, firstName, lastName, userName, email, password)
