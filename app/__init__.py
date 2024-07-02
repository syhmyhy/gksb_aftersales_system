#app\__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import filters  # Import your custom filters module

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')  # Load app configurations from config.py
db = SQLAlchemy(app)

# Register custom filters
app.jinja_env.filters['format_rm_currency'] = filters.format_rm_currency
app.jinja_env.filters['dateformat'] = filters.dateformat

# Importing all the view modules
from app import models, view_home, view_job, view_aftersales, view_staff, view_auth, view_sales
