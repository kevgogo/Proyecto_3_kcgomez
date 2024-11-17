import shutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, inspect
from pymysql import OperationalError

from app.data_loader import cargar_datos
from app.utils import conditional_print
from app.extensions import db
from config import Config

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = Config.database_uri()
conditional_print(f"Final SQLALCHEMY_DATABASE_URI: {Config.database_uri()}")

db.init_app(app)
conditional_print("SQLAlchemy initialized successfully.")

with app.app_context():
    try:
        connection = db.engine.connect()
        conditional_print("Database connection successful.")
        connection.close()
    except Exception as e:
        conditional_print(f"Database connection failed: {e}")

    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if tables:
            conditional_print(f"Existing tables: {tables}")
            db.drop_all() 
        else:
            conditional_print("No tables found. Ready to create tables.")
        db.create_all() 
        cargar_datos()
    except Exception as e:
        conditional_print(f"Error with inspector or database operations: {e}")

from app import routes