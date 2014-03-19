from flask import render_template
from python import app

@app.route('/')
@app.route('/index')
def index():

	events = [ # dummy array of events
        {
            'name': 'EOH 2014',
			'time': '3/19/2014, 1:45pm',
			'location': 'engineering campus',
			'food': 'subway'
        },
		{
            'name': 'CS After Hours',
			'time': '3/20/2014, 4:30pm',
			'location': 'Seibel center',
			'food': 'maize'
        },
		{
            'name': 'Career fair',
			'time': '3/24/2014, 11:00am',
			'location': 'illini union',
			'food': 'various'
        },
		{
            'name': 'reflections projections',
			'time': '4/10/2014, 12:00pm',
			'location': 'Seibel center',
			'food': 'pizza'
        },
		{
            'name': 'Bring your family day',
			'time': '4/14/2014, 10:00am',
			'location': 'engineering campus',
			'food': 'chipotle'
        }

    ]

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
