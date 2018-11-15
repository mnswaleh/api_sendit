"""Configure application"""
import os

DEBUG = True  # Turns on debugging features in Flask
CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
