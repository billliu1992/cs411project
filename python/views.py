from flask import render_template, request, redirect, session, flash, url_for
from flask.ext.login import login_user, current_user, login_required, logout_user
from python import app, lm
from facepy.exceptions import FacebookError

from python.db.common import *
from python.db.eventutil import EventUtil
from python.db.userutil import UserUtil
from python.db.locationutil import LocationUtil
from python.db.foodutil import FoodUtil

from python.obj.user import User
from python.obj.form import RegistrationForm

from python.crawl.fbutil import FacebookUtil
from python.crawl.crawlutil import CrawlUtil

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
		
		if not(current_user.is_authenticated()):
			event_body['prefers'] = False
		else:
			event_body['prefers'] = prefers(event)
			
		events.append(event_body)
		
	events.reverse()
		
	return render_template("index.html", events=events)

def prefers(event):
	user = UserUtil.get_user(current_user.userId)
	for food in user.food_pref:
		if event.food != None and food.foodId == event.food.foodId:
			return True
	for location in user.location_pref:
		if event.location != None and location.locationId == event.location.locationId:
			return True
	return False
	
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
			flash("Logged in successfully.", "success")
			return redirect(url_for('index'))
		else:
			flash("Unable to login, please try again.", "danger")

	return render_template("sign_in.html")

@app.route('/logout')
@login_required
def logout():
	user = current_user
	user.authenticate(False)
	logout_user()

	flash("Logged out successfully.", "success")
	return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST'])
def sign_up():
	form = RegistrationForm(request.form)

	if request.method == 'POST' and form.validate():
		new_user = UserUtil.create_user(form.username.data, form.email.data,
				form.password.data)
		flash("Thanks " + new_user.userName + " for registering", "success")
		return redirect(url_for('sign_in'))

	return render_template("sign_up.html", form=form)

@app.route('/view/<id>',methods=['GET','POST'])
def event_view(id):
	if request.method == 'GET':
		event = EventUtil.get_event(id)
		if(event == None):
			flash("That event does not exist!", "danger")
			return redirect("/")
			
		return render_template("event_view.html", event=event)

@app.route('/edit/<id>',methods=['GET','POST'])
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
			event.location = LocationUtil.get_location(int(locationid))
			
		if(foodid.isdigit()):
			event.food = FoodUtil.get_food(int(foodid))
			
		event.food.foodName = request.form['event_food_name']
		
		event.name = request.form['event_name']
		
		if(request.form['event_time'] != ""):
			try:
				event_date = convert_str_to_datetime(request.form['event_time'])
				event.time = event_date
			except ValueError:
				flash("You entered a datetime of the wrong format. The required format is: %Y-%m-%d %H:%M:%S")
				return redirect('/edit/' + id)
		
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
			event.location = LocationUtil.get_location(int(locationid))
			
		if(foodid.isdigit()):
			event.food = FoodUtil.get_food(int(foodid))
			
		event.name = request.form['event_name']

		if(request.form['event_time'] != ""):
			try:
				event_date = convert_str_to_datetime(request.form['event_time'])
				event.time = event_date
			except ValueError:
				flash("You entered a datetime of the wrong format. The required format is: %Y-%m-%d %H:%M:%S")
				return redirect('/edit/' + id)
		
		EventUtil.update_event(event)

		return redirect('/index')
	
@app.route('/delete_<id>')
def event_delete(id=None):
	EventUtil.delete_event(id)
	return redirect('/index')

@app.route('/preferences',methods=['GET','POST'])
@login_required
def preferences():
	if request.method == 'GET':
		all_locations = LocationUtil.get_all_locations_array()
		foods = FoodUtil.get_all_foods_array()

		user = UserUtil.get_user(current_user.userId)
		
		selected_locations = []
		
		for selected_loc_obj in user.location_pref:
			selected_locations.append(selected_loc_obj.locationId)
			
		selected_foods = []
		for selected_food_obj in user.food_pref:
			selected_foods.append(selected_food_obj.foodId)
		
		return render_template("preferences.html",all_locations=all_locations,foods=foods,selected_locations=selected_locations,selected_foods=selected_foods)
	else:
		current_user_obj = UserUtil.get_user(current_user.userId)
		
		new_locations = []
		for location in request.form.getlist('location-prefs'):
			new_locations.append(LocationUtil.get_location(location))
			
		
		current_user_obj.location_pref = new_locations
		
		new_foods = []
		for food in request.form.getlist('food-prefs'):
			new_foods.append(FoodUtil.get_food(food))
				
		current_user_obj.food_pref = new_foods
		
		UserUtil.update_user_food_prefs(current_user_obj)
		UserUtil.update_user_loc_prefs(current_user_obj)
				
		return redirect('/')
		
@app.route('/import/', methods=["GET", "POST"])
def import_facebook():
	if(request.method == "GET"):
		if current_user.is_authenticated():
			return render_template("import_facebook.html")
		else:
			flash("You must be logged in to use this feature", "danger")
			return redirect("/login")
	else:
		facebook_url = request.form["event-url"]
		
		eventId = FacebookUtil.url_get_event_id(facebook_url)
		
		#validate event url
		if(eventId == None):
			flash("You must enter a valid Facebook event URL of the format https://www.facebook.com/events/...", "danger")
			return redirect("/import/")
			
		#validate event id
		try:
			event_dict = FacebookUtil.get_event_dict(eventId)
		except FacebookError as e:
			flash("e.strerror")
			return redirect("/import/")
		
		is_free = CrawlUtil.is_free_food(event_dict["description"])
		
		#make sure it is a free food event
		if(not is_free):
			flash("The description did not mention free food and/or mentioned entrance fees. Please only import events featuring free food", "danger")
			return redirect("/import/")
			
		food = CrawlUtil.guess_food_type(event_dict["description"])
		foodId = None
		if(food != None):
			foodId = food.foodId
		if(event_dict["is_date_only"]):
			start_time = convert_str_to_date(event_dict["start_time"])
		else:
			start_time = convert_str_to_datetime_fb(event_dict["start_time"][:len(event_dict["start_time"])-5])
		location = CrawlUtil.get_location_or_create(event_dict["location"], event_dict["venue"]["street"] + " " + event_dict["venue"]["city"] + ", " + event_dict["venue"]["state"])
		
		#make sure it isn't a duplicate
		if(not CrawlUtil.has_no_duplicate(start_time, location.locationId, foodId)):
			flash("This event already exists!", "danger")
			return redirect("/import/")
		
		new_event = EventUtil.create_event()
		new_event.food = food
		new_event.name = event_dict["name"]
		new_event.time = start_time 
		new_event.location = location
		new_event.organizer = current_user
		
		EventUtil.update_event(new_event)
		
		
		flash("Successfully imported Facebook event", "success")
		return redirect("/")
