#app\__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')  # Load app configurations from config.py

db = SQLAlchemy(app)

from app import models, view_home, view_job, view_aftersales, view_staff, view_auth