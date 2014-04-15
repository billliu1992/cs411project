from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)

app.secret_key = "cs411project"
from python import views
