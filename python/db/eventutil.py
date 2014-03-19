from common import *
from obj.event import Event
import datetime

class EventUtil:
	@staticmethod
	def create_event():
		"""
		Creates an event in the database, and returns an object for the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		
		result = cursor.execute("""
			INSERT INTO Event (foodId, locationId, name, organizer, startTime)
			VALUES (NULL, NULL, "", NULL, NULL);
			""")
			
		if(len(result) != None):
			return Event(result[0])
		else:
			print("Error creating event")
	
		connection.commit()
		connection.close()
		
	@staticmethod
	def update_event(event_obj):
		"""
		Updates the event in the database only if the event exists
		"""
		if(not isinstance(event_obj, Event)):
			print("Passed in wrong object when updating event")
		
		connection = connection_to_db()
		cursor = connection.cursor()
		
		#grab data from the objects
		eventId = event_obj.eventId
		
		locationId = None
		if(not event_obj.location == None):
			locationId = event_obj.location.locationId
		
		foodId = None
		if(not eventId.food == None):
			foodId = event_obj.food.foodId
		
		organizerId = None
		if(not event_obj.organizer == None):
			organizerId = event_obj.organizer.organizerId
		
		result = cursor.execute("""
			UPDATE Event SET
			foodId = %s,
			locationId = %s,
			name = %s,
			organizerId = %s,
			startTime = %s
			WHERE
			eventId = %s;
			""", (str(foodId), str(locationId), eventId.name, str(organizerId), convert_datetime(eventId.time)))
			
		connection.commit()
		connection.close()
	
	@staticmethod
	def get_event(eventId):
		connection = connection_to_db()
		cursor = connection.cursor()
		
		result = cursor.execute("""
			SELECT * FROM Event WHERE
			eventId = %s
			""", (eventId))
		
		return convert_array_to_obj(result)
	
	@staticmethod
	def get_events_by_food(food_obj):
		foodId = food_obj.foodId
		connection = connection_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			foodId = %s
			""", (foodId))
			
		result = cursor.fetchall()
		for(row in result):
			return convert_array_to_obj(row)
			
	@staticmethod
	def get_events_by_location(location_obj):
		locationId = location_obj.locationId
		connection = connection_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			locationId = %s
			""", (locationId))
				
		result = cursor.fetchall()
		for(row in result):
			return convert_array_to_obj(row)
			
	@staticmethod
	def get_events_by_organizer(organizer_obj):
		organizerId = organizer_obj.organizerId
		connection = connection_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			organizerId = %s
			""", (organizerId))
	
		result = cursor.fetchall()
		for(row in result):
			return convert_array_to_obj(row)
	
	@staticmethod
	def convert_array_to_obj(array):
		eventId, foodId, locationId, name, organizerId, startTime = array
		food_obj = FoodUtil.get_food(foodId)
		location_obj = LocationUtil.get_location(locationId)
		organizer_obj = UserUtil.get_user(organizerId)
		date_obj = datetime.mktime(datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S'))
		
		return Event(eventId, name, date_obj, location_obj, food_obj, organizer_obj)
