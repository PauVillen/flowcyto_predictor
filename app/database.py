## script to initialize the db object independently to avoid errors when adding more functions

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()