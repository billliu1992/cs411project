from common import *
from python.obj.user import User
from python.db.locationutil import LocationUtil
from python.db.foodutil import FoodUtil
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
		UserUtil.user_dict[userId] = user

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
				new_user_obj.location_pref = UserUtil.get_user_loc_prefs(new_user_obj)
				new_user_obj.food_pref = UserUtil.get_user_food_prefs(new_user_obj)
				UserUtil.user_dict[userId] = new_user_obj
				return new_user_obj
			else:
				print("User: " + str(userId) + " does not exist")
				return None
		else:
			return UserUtil.user_dict[userId]
			
	@staticmethod
	def get_user_loc_prefs(user_obj):
	
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM LocationPref WHERE userId = %s
			""", (user_obj.userId,))
		
		results = cursor.fetchall()
	
		location_objs = []
		for result in results:
			location_objs.append(LocationUtil.get_location(result[0]))

		return location_objs
		
	@staticmethod
	def update_user_loc_prefs(user_obj):
	
		connection = connect_to_db()
	
		prev_prefs = UserUtil.get_user_loc_prefs(user_obj)
		
		#add everything that needs to be added
		for curr_pref in user_obj.location_pref:
			needs_insert = True
			for prev_pref in prev_prefs:
				if(prev_pref.locationId == curr_pref.locationId):
					needs_insert = False
			
			if(needs_insert == True):
				cursor = connection.cursor()
				cursor.execute("INSERT INTO LocationPref VALUES (%s, %s)", (curr_pref.locationId, user_obj.userId))
				
		#remove everything that needs to be removed
		for prev_pref in prev_prefs:
			needs_delete = True
			for curr_pref in user_obj.location_pref:
				if(prev_pref.locationId == curr_pref.locationId):
					needs_insert = False
			
			if(needs_delete == True):
				cursor = connection.cursor()
				cursor.execute("DELETE FROM LocationPref WHERE locationId = %s AND userId = %s", (curr_pref.locationId, user_obj.userId))
				
		connection.commit()
		connection.close()
		
		
	@staticmethod
	def get_user_food_prefs(user_obj):
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM FoodPref WHERE userId = %s
			""", (user_obj.userId,))
		results = cursor.fetchall()
	
		food_objs = []
		for result in results:
			food_objs.append(FoodUtil.get_food(result[0]))

		return food_objs
		
	@staticmethod
	def update_user_food_prefs(user_obj):
	
		connection = connect_to_db()
	
		prev_prefs = UserUtil.get_user_food_prefs(user_obj)
		
		#add everything that needs to be added
		for curr_pref in user_obj.food_pref:
			needs_insert = True
			for prev_pref in prev_prefs:
				if(prev_pref.foodId == curr_pref.foodId):
					needs_insert = False
			
			if(needs_insert == True):
				cursor = connection.cursor()
				cursor.execute("INSERT INTO FoodPref VALUES (%s, %s)", (curr_pref.foodId, user_obj.userId))
				
		#remove everything that needs to be removed
		for prev_pref in prev_prefs:
			needs_delete = True
			for curr_pref in user_obj.food_pref:
				if(prev_pref.foodId == curr_pref.foodId):
					needs_insert = False
			
			if(needs_delete == True):
				cursor = connection.cursor()
				cursor.execute("DELETE FROM LocationPref WHERE locationId = %s AND userId = %s", (prev_pref.foodId, user_obj.userId))
				
		connection.commit()
		connection.close()
		

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
