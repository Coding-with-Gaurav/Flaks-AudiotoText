from flask import Flask
from flask_pymongo import PyMongo
from config import config
from pymongo import MongoClient

mongo = PyMongo()

def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    print(f"MONGO_URI: {app.config['MONGO_URI']}")  
    
    app.static_folder = 'static'
    app.template_folder = 'templates'

    mongo.init_app(app)

    try:
        client = mongo.cx
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    # Test MongoDB connection
    uri = app.config['MONGO_URI']
    client = MongoClient(uri)
    db = client.get_database()
    print(f"Connected to MongoDB: {db.name}")


    # Import and register routes with the Flask app and the mongo object
    from app.routes import register_routes
    register_routes(app, mongo)

    return app
