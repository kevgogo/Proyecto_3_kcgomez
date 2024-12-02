import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)
    APP_ENV = os.getenv('APP_ENV', 'development')
    ENABLE_PRINTS = os.getenv('ENABLE_PRINTS', 'false').lower() == 'true'
    TESTING = os.getenv('TESTING', 'false').lower() == 'true'
    API_PREFIX = os.getenv('API_PREFIX', 'api')
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'false').lower() == 'true'
    
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  # Duración de 1 hora
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Duración de 1 hora

    # Database Configuration
    NAME_DB = os.getenv('NAME_DB', 'heladeria')

    @staticmethod
    def database_uri():
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.makedirs(os.path.join(basedir, "db"), exist_ok=True)
        db_path = os.path.join(
            basedir, 
            "db", 
            f"{'test_' + Config.NAME_DB if Config.TESTING else Config.NAME_DB}.db"
        )
        return f"sqlite:///{db_path}"
    
    @staticmethod
    def URLBuilder(metodo):
        from flask import request
        return f"{request.host_url.rstrip('/')}/{Config.API_PREFIX}/{metodo}"
    
    @staticmethod
    def conditional_print(message):
        if Config.ENABLE_PRINTS:
            print(f" * {message}")