from flask import render_template, request, redirect, session
from python import app

from python.db.common import *
from python.db.eventutil import EventUtil
from python.db.userutil import UserUtil
from python.db.locationutil import LocationUtil
from python.db.foodutil import FoodUtil

@app.route('/')
@app.route('/index')
def index():

	#Database stuff
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
		event_body['eventId'] = event.eventId

		events.append(event_body)
		
	return render_template("index.html", events=events)
		
@app.route('/user_page')
def user_page():
	return render_template("user_page_modify.html", user='sally')

@app.route('/login')
def sign_in():
	return render_template("sign_in.html")

@app.route('/authenticate', methods=["POST"])
def authenticate_user():
	if(UserUtil.authenticate(request.form["email"], request.form["passwd"])):
		session["logged_in_user"] = request.form["email"]
		return redirect("/")
	else:
		return redirect("/login")

@app.route('/join')
def sign_up():
	return render_template("sign_up.html")
	
@app.route('/create_new', methods=["POST"])
def create_new_user():
	new_user = UserUtil.create_user()
	new_user.userName = request.form["username"]
	new_user.email = request.form["email-addr"]
	new_user.password = request.form["password"]
	UserUtil.update_user(new_user)
	
	session["logged_in_user"] = request.form["username"]
	
	return redirect("/")


@app.route('/edit_<id>',methods=['GET','POST'])
def event_edit(id=None):
	if request.method == 'GET':
		event = EventUtil.get_event(id)
		return render_template("event_edit.html",event=event)
	else:
		event = EventUtil.get_event(id)
		event.location.name = request.form['event_location_name']
		event.location.address = request.form['event_location_address']
		event.location.gps_coord = request.form['event_location_gpsAddress']
		event.food.foodName = request.form['event_food_name']
		event.name = request.form['event_name']
		
		EventUtil.update_event(event)

		return redirect('/index')

@app.route('/edit_new',methods=['GET','POST'])
def event_new():
	if request.method == 'GET':
		return render_template("event_new.html")
	else:
		event = EventUtil.create_event()
		event.location = LocationUtil.create_location()
		event.location.name = request.form['event_location_name']
		event.location.address = request.form['event_location_address']
		event.location.gps_coord = request.form['event_location_gpsAddress']
		event.food = FoodUtil.create_food()
		event.food.foodName = request.form['event_food_name']
		event.name = request.form['event_name']
		
		LocationUtil.update_location(event.location)
		FoodUtil.update_food(event.food)
		EventUtil.update_event(event)

		return redirect('/index')
	
@app.route('/delete_<id>')
def event_delete(id=None):
	event = EventUtil.delete_event(id)
	return redirect('/index')
