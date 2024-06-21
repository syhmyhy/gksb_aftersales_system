#config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
