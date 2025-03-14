# app/__init__.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.config.connect import db
from app.jobs.routes import jobsapi

def create_app():
    # Load environment variables from .env
    load_dotenv()
    
    app = Flask(__name__)
    CORS(app)
    
    # Fetch database configuration from environment variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")
    
    # Construct the SQLAlchemy connection string with SSL mode enabled
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    
    # Configure the Flask app for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Optionally, test the connection (this will print to the console)
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")
    
    # Register blueprints
    app.register_blueprint(jobsapi)
    
    # Handle 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Not Found"}), 404
    
    return app
