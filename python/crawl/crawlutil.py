import re

from python.db.foodutil import FoodUtil
from python.obj.food import Food
from python.db.locationutil import LocationUtil

class CrawlUtil:
	
	good_words = ["free", "food", "drinks", "complimentary", "provided"]
	bad_words = ["$", "cost", "costs", "fee"]
	
	@staticmethod
	def is_free_food(description_str):
		"""
		Takes a description and returns a decision on whether or not it thinks there is free food
		"""
		description_str = description_str.lower()	#do not want to worry about case
		
		score = 0	#we keep track of how many good words were found compared to how many bad words were found
		
		for word in DescriptionParser.good_words:
			if(word in description_str):
				score += 1
				
		food_arr = FoodUtil.get_all_foods_array()
		
		for food_type in food_arr:
			if("free " + food_type[1] in description_str):
				score += 2
				
		for word in DescriptionParser.bad_words:
			if(word in description_str):
				score -= 1
		
		print score
				
		if(score > 0):
			return True
		else:
			return False
			
	@staticmethod
	def guess_food_type(description_str):
		"""
		Takes a description of an event with free food and attempts to guess which category of food it will have
		"""
		
		description_str = description_str.lower()
		
		food_arr = FoodUtil.get_all_foods_array()
		
		for food_type in food_arr:
			if(food_type[1] in description_str):
				return FoodUtil.get_food(food_type[0])

		return None
		
		
		
	@staticmethod
	def get_location_or_create(location_str, address=None):
		"""
		Either returns a previously created location or creates a location in the database
		"""
		
		location_arr = LocationUtil.get_all_locations_array()
		
		for location in location_arr:
			if(is_similar(location_str, location[1])):
				return LocationUtil.get_location(location[0])

		#not found similar one in the database, therefore create
		new_location = LocationUtil.create_location()
		new_location.name = location_str
		if(address != None):
			new_location.address = address
			
		LocationUtil.update_location(new_location)
		
		return None
		
	@staticmethod
	def is_similar(location_str1, location_str2):
		"""
		Returns True if the two location names are deemed similar
		"""
		location_name1 = location_str1.lower()
		location_name1 = re.sub("[^\d\w ]|(?:the )", "", location_name1)
		
		print(location_str1 + " turns into: " + location_name1)
		
		location_name2 = location_str2.lower()
		location_name2 = re.sub("[^\d\w ]|(?:the )", "", location_name2)
		
		print(location_str2 + " turns into: " + location_name2)
		
		if(location_name1 in location_name2):
			return True
			
		if(location_name2 in location_name1):
			return True
			
		#Maybe do more?
		
		return False
		
		
