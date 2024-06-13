# app/__init__.py

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from config import config

# Load environment variables from .env file
load_dotenv()

mongo = PyMongo()

def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(config[config_name])

    # Configure paths to static and template files
    app.static_folder = 'static'
    app.template_folder = 'templates'

    # Initialize MongoDB
    mongo.init_app(app)

    # Import and register routes
    from app.routes import register_routes
    register_routes(app)

    return app
