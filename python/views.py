from flask import render_template, request, redirect, session
from python import app

from python.db.common import *
from python.db.eventutil import EventUtil
from python.db.userutil import UserUtil

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


@app.route('/event_edit')
def event_edit():
	return render_template("event_edit.html")
