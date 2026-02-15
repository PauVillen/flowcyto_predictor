## este script solo es para inicalizar el objeto db de forma independiente para evitar errores cuando vayamos añadiento más funciones

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()