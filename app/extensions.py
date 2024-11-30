from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()