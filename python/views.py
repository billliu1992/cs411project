from flask import render_template
from python import app

from python.db.common import *
from python.db.eventutil import EventUtil

@app.route('/')
@app.route('/index')
def index():

	connection = connect_to_db()
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM Event")

	results = cursor.fetchall()

	events = []

	for result in results:
		event = EventUtil.convert_array_to_obj(result)

		event_body = {}
		event_body['name'] = event.name
		event_body['time'] = event.time
		event_body['location'] = event.location
		event_body['food'] = event.food

		events.append(event_body)

	return render_template("index.html", events=events)

@app.route('/user_page')
def user_page():
	return render_template("user_page_modify.html", user='sally')

@app.route('/login')
def sign_in():
	return render_template("sign_in.html")

@app.route('/join')
def sign_up():
	return render_template("sign_up.html")
