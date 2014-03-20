from common import *
from python.obj.food import Food
import datetime

class FoodUtil:
	food_dict = {}
	
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
		
		food_created = Food(connection.insert_id())
		FoodUtil.food_dict[food_created.foodId] = food_created
		return food_created
			        
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
			foodName = %s
			WHERE
			foodId = %s;
			""", (food_obj.foodName, food_obj.foodId))
		                    
		connection.commit()
		connection.close()
		            
	@staticmethod
	def get_food(foodId):
		if not foodId in FoodUtil.food_dict:
			connection = connect_to_db()
			cursor = connection.cursor()
			            
			cursor.execute("""
				SELECT * FROM Food WHERE
				foodId = %s
				""", (foodId,))
			                      
			result = cursor.fetchall()
			            
			if(len(result) > 0):
				new_food = FoodUtil.convert_array_to_obj(result[0])
				FoodUtil.food_dict[foodId] = new_food
				return new_food
			else:
				print("Food type: " + str(foodId) + " does not exist")
				return None
		else:
			return FoodUtil.food_dict[foodId]
		                      
	@staticmethod
	def convert_array_to_obj(array):
		foodId, foodName = array
		return Food(foodId, foodName)
