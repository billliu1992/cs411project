import MySQLdb
import datetime, time

def connect_to_db():
	"""
	Returns a db connection
	"""
	hostname = "mysql.server"
	usr_name = "billliu1992"
	usr_password = "cs411project"
	db_name = "billliu1992$freefood"

	connection = MySQLdb.connect(host = hostname, user = usr_name, passwd = usr_password, db = db_name)
	
	return connection
	
def convert_datetime_to_str(datetime_obj):
	if(datetime_obj == None):
		return None
	return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
	
def convert_str_to_datetime(date_str):
	if(date_str == None):
		return None
	return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
