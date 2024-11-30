import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    APP_ENV = os.getenv('APP_ENV', 'development')
    ENABLE_PRINTS = os.getenv('ENABLE_PRINTS', 'false').lower() == 'true'
    TESTING = os.getenv('TESTING', 'false').lower() == 'true'
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    
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