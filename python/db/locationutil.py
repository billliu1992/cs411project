from common import *
from python.obj.location import Location
import datetime

class LocationUtil:

	location_dict = {}

	@staticmethod
	def create_location():
		"""
		Creates an location in the database, and returns an object for the user to manipulate
		"""
		connection = connect_to_db()
		cursor = connection.cursor()
		
		cursor.execute("""
			INSERT INTO Location (name, address, gpsAddr)
			VALUES ("", NULL, NULL);
			""")
			
		connection.commit()
		LocationUtil.location_dict[connection.insert_id()] = Location(connection.insert_id())
		return location_dict[connection.insert_id()]
		
	@staticmethod
	def update_location(location_obj):
		"""
		Updates the location in the database only if the location exists
		"""
		if(not isinstance(location_obj, Location)):
			print("Passed in wrong object when updating location")
		
		connection = connect_to_db()
		cursor = connection.cursor()
		
		
		result = cursor.execute("""
			UPDATE Location SET
			name = %s,
			address = %s,
			gpsAddr = %s
			WHERE
			locationId = %s;
			""", (location_obj.name, location_obj.address, location_obj.gps_coord, location_obj.locationId))
		
		connection.commit()
		connection.close()
		
	@staticmethod
	def get_location(locationId):
	
		if not locationId in LocationUtil.location_dict:
			connection = connect_to_db()
			cursor = connection.cursor()
		
			cursor.execute("""
				SELECT * FROM Location WHERE
				locationId = %s
				""", (locationId,))
		
			result = cursor.fetchall()
		
			if(len(result) > 0):
				new_location_obj = LocationUtil.convert_array_to_obj(result[0])
				
				LocationUtil.location_dict[locationId] = new_location_obj
				return new_location_obj
			else:
				print("Location: " + str(locationId) + " does not exist")
				return None
		else:
			return LocationUtil.location_dict[locationId]
			
	@staticmethod
	def convert_array_to_obj(array):
		locationId, name, address, gps_coord = array
		return Location(locationId, name, address, gps_coord)
