'''
Created on Mar 13, 2014
A class storing data about the 
location of each event
@author: Will
'''
class Location():
	def __init__(self, locationId, name = "", address = "", gps_coord = ""):
		self.locationId = locationId
		self.name = name
		self.address = address
		self.gps_coord = gps_coord
