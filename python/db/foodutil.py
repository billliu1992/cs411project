from common import *
from python.obj.food import Food
import datetime

class FoodUtil:
	@staticmethod
	def create_food():
		"""
		Enters food in the database, and returns an object for the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		          
		cursor.execute("""
			INSERT INTO Food (foodName)
			VALUES (NULL);
			""")
		
		connection.commit()
		return Food(connection.insert_id())
			        
	@staticmethod
	def update_food(food_obj):
		"""
		Updates the food in the database only if the food exists
		"""
		if(not isinstance(food_obj, Food)):
			print("Passed in wrong object when updating location")
		                    
		connection = connect_to_db()
		cursor = connection.cursor()
		            
		            
		result = cursor.execute("""
			UPDATE Food SET
			foodName = %s,
			WHERE
			foodId = %s;
			""", (food_obj.name, food_obj.foodId))
		                    
		connection.commit()
		connection.close()
		            
	@staticmethod
	def get_food(foodId):
		connection = connect_to_db()
		cursor = connection.cursor()
		            
		cursor.execute("""
			SELECT * FROM Food WHERE
			foodId = %s
			""", (foodId,))
		                      
		result = cursor.fetchall()
		            
		if(len(result) > 0):
			return FoodUtil.convert_array_to_obj(result[0])
		else:
			print("Food type: " + str(foodId) + " does not exist")
			return None
		                      
	@staticmethod
	def convert_array_to_obj(array):
		foodId, foodName = array
		return Food(foodId, foodName)