import MySQLdb

def connect_to_db():
	hostname = "engr-cpanel-mysql.engr.illinois.edu"
	usr_name = "teamtemplate_web"
	usr_password = "cs411project"
	db_name = "teamtemplate_freefood"

	connection = MySQLdb.connect(host = hostname, user = usr_name, passwd = usr_password, db = db_name)
