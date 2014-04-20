from flask import render_template, request, redirect, session, flash, url_for
from flask.ext.login import login_user, current_user, login_required, logout_user
from python import app, lm

from python.db.common import *
from python.db.eventutil import EventUtil
from python.db.userutil import UserUtil
from python.db.locationutil import LocationUtil
from python.db.foodutil import FoodUtil

from python.obj.user import User
from python.obj.form import RegistrationForm

@lm.user_loader
def load_user(username):
	return User.get(username)

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
		event_body['eventId'] = event.eventId

		events.append(event_body)
		
	return render_template("index.html", events=events)
		
@app.route('/user_page')
def user_page():
	return render_template("user_page_modify.html", user='sally')

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
	if request.method == 'POST':
		username=request.form['email']
		password=request.form['passwd']

		user=User.get(username)

		if user and user.password == password:
			user.authenticate()
			login_user(user, remember=True)
			flash("Logged in successfully.")
			return redirect(url_for('index'))
		else:
			flash("Unable to login, please try again.")

	return render_template("sign_in.html")

@app.route('/logout')
@login_required
def logout():
	user = current_user
	user.authenticate(False)
	logout_user()

	flash("Logged out successfully.")
	return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST'])
def sign_up():
	form = RegistrationForm(request.form)

	if request.method == 'POST' and form.validate():
		new_user = UserUtil.create_user(form.username.data, form.email.data,
				form.password.data)
		flash("Thanks " + new_user.userName + " for registering")
		return redirect(url_for('sign_in'))

	return render_template("sign_up.html", form=form)
	
@app.route('/edit_<id>',methods=['GET','POST'])
def event_edit(id=None):
	if request.method == 'GET':
		event = EventUtil.get_event(id)
		all_foods = FoodUtil.get_all_foods_array()
		all_locations = LocationUtil.get_all_locations_array()
		
		return render_template("event_new.html", event=event, all_locations=all_locations, all_foods=all_foods)
	else:
		event = EventUtil.get_event(id)
		
		locationid = request.form["locationId"]
		foodid = request.form["foodId"]
		
		if(locationid.isdigit()):
			print(locationid)
			event.location = LocationUtil.get_location(int(locationid))
			
		if(foodid.isdigit()):
			print(foodid)
			event.food = FoodUtil.get_food(int(foodid))
			
		event.food.foodName = request.form['event_food_name']
		
		event.name = request.form['event_name']
		
		EventUtil.update_event(event)

		return redirect('/index')

@app.route('/new_location', methods=['GET', 'POST'])
def new_location():
	if(request.method == 'GET'):
		return render_template("location_new.html")
	else:
		new_location = LocationUtil.create_location()
		new_location.name = request.form['name']
		new_location.address = request.form['address']
		#event.location.gps_coord = request.form['event_location_gpsAddress']
		LocationUtil.update_location(new_location)
	
		return redirect("/index")

@app.route("/new_food", methods=['GET', 'POST'])
def new_food():
	if(request.method == 'GET'):
		return render_template("food_new.html")
	else:
		new_food = FoodUtil.create_food()
		new_food.foodName = request.form['name']
		FoodUtil.update_food(new_food)
		return redirect("/index")

@app.route('/edit_new',methods=['GET','POST'])
def event_new():
	if request.method == 'GET':
		event = EventUtil.get_event(id)
		all_foods = FoodUtil.get_all_foods_array()
		all_locations = LocationUtil.get_all_locations_array()
		
		return render_template("event_new.html", event=event, all_locations=all_locations, all_foods=all_foods)
	else:
		event = EventUtil.create_event()
		
		locationid = request.form["locationId"]
		foodid = request.form["foodId"]
		
		if(locationid.isdigit()):
			print(locationid)
			event.location = LocationUtil.get_location(int(locationid))
			
		if(foodid.isdigit()):
			print(foodid)
			event.food = FoodUtil.get_food(int(foodid))
			
		event.food.foodName = request.form['event_food_name']
		
		event.name = request.form['event_name']
		
		EventUtil.update_event(event)

		return redirect('/index')
	
@app.route('/delete_<id>')
def event_delete(id=None):
	event = EventUtil.delete_event(id)
	return redirect('/index')

@app.route('/preferences',methods=['GET','POST'])
def preferences():
	if request.method == 'GET':
		all_locations = LocationUtil.get_all_locations_json()
		return render_template("preferences.html",all_locations=all_locations)
	else:
		return redirect('/index');

