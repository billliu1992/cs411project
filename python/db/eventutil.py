from common import *
from python.obj.event import Event
import datetime

from locationutil import LocationUtil
from foodutil import FoodUtil
from userutil import UserUtil

class EventUtil:
	events_dict= {:}
	
	@staticmethod
	def create_event():
		"""
		Creates an event in the database, and returns an object for the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			INSERT INTO Event (foodId, locationId, name, organizerId, startTime)
			VALUES (NULL, NULL, "", NULL, NULL);
			""")
			
		connection.commit()
		event_created = Event(connection.insert_id())
		events_dict[event_created.eventId] = event_created
		return event_created
		
	@staticmethod
	def update_event(event_obj):
		"""
		Updates the event in the database only if the event exists
		"""
		if(not isinstance(event_obj, Event)):
			print("Passed in wrong object when updating event")
		
		connection = connect_to_db()
		cursor = connection.cursor()
		
		#grab data from the objects
		eventId = event_obj.eventId
		
		locationId = None
		if(not event_obj.location == None):
			locationId = event_obj.location.locationId
		
		foodId = None
		if(not event_obj.food == None):
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
			""", (str(foodId), str(locationId), event_obj.name, str(organizerId), convert_datetime_to_str(event_obj.time), eventId))
		
		connection.commit()
		connection.close()
	
	@staticmethod
	def get_event(eventId):
		if eventId in events_obj:
			
			connection = connect_to_db()
			cursor = connection.cursor()
			
			cursor.execute("""
				SELECT * FROM Event WHERE
				eventId = %s
				""", (eventId,))
			
			result = cursor.fetchall()
			
			if(len(result) > 0):
				return EventUtil.convert_array_to_obj(result[0])
			else:
				print("Event: " + str(eventId) + " does not exist")
				return None
		else:
			event_to_return = EventUtil.convert_array_to_obj(result[0])
			events_dict[eventId] = event_to_return
	
	@staticmethod
	def get_events_by_food(food_obj):
		foodId = food_obj.foodId
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			foodId = %s
			""", (foodId))
			
		result = cursor.fetchall()
		for row in result:
			return convert_array_to_obj(row)
			
	@staticmethod
	def get_events_by_location(location_obj):
		locationId = location_obj.locationId
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			locationId = %s
			""", (locationId))
				
		result = cursor.fetchall()
		for row in result:
			return convert_array_to_obj(row)
			
	@staticmethod
	def get_events_by_organizer(organizer_obj):
		organizerId = organizer_obj.organizerId
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			SELECT * FROM Event WHERE
			organizerId = %s
			""", (organizerId))
	
		result = cursor.fetchall()
		for row in result:
			return convert_array_to_obj(row)
	
	@staticmethod
	def convert_array_to_obj(array):
		eventId, locationId, foodId, organizerId, name, startTime = array
		location_obj = LocationUtil.get_location(locationId)
		food_obj = FoodUtil.get_food(foodId)
		organizer_obj = UserUtil.get_user(organizerId)
		#date_obj = convert_str_to_datetime(startTime)
		
		return Event(eventId, name, startTime, location_obj, food_obj, organizer_obj)
