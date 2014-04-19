from common import *
from python.obj.user import User
import datetime

class UserUtil:

	user_dict = {}

	@staticmethod
	def create_user(userName, email, password):
		"""
		Creates an user in the database, and returns an object for 
		the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			INSERT INTO User (firstName, lastName, userName, email, password)
			VALUES ("", "", %s, %s, %s);
			""", (userName, email, password))
			
		connection.commit()
		userId = connection.insert_id()
		connection.close()

		user = User(userId, "", "", userName, email, password, False)
		UserUtil.user_dict[userid] = user

		return user
		
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
			firstName = %s,
			lastName  = %s,
			userName  = %s,
			email = %s,
			password  = %s
			WHERE userId = %s;
			""", (user_obj.firstName, user_obj.lastName, user_obj.userName,
				user_obj.email, user_obj.password, user_obj.userId))
		
		connection.commit()
		connection.close()
		
	@staticmethod
	def get_user(userId):
		if(not userId in UserUtil.user_dict):
			connection = connect_to_db()
			cursor = connection.cursor()
		
			cursor.execute("""
				SELECT * FROM User WHERE
				userId = %s
				""", (userId,))
		
			result = cursor.fetchone()
		
			if result:
				new_user_obj = UserUtil.convert_array_to_obj(result)
				UserUtil.user_dict[userId] = new_user_obj
				return new_user_obj
			else:
				print("User: " + str(userId) + " does not exist")
				return None
		else:
			return UserUtil.user_dict[userId]
		

	@staticmethod
	def authenticate(username, passwd):
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM User
			""")
			
		results = cursor.fetchall()		
	
		in_db = False
	
		for result in results:
			email, firstName, lastName, password, userId, userName = result
			if((username == userName or username == email) and password == passwd):
				in_db = True
				
		return in_db
	
	@staticmethod
	def convert_array_to_obj(array):
		userId, firstName, lastName, userName, email, password, authenticated = array
		return User(userId, firstName, lastName, userName, email, password)
