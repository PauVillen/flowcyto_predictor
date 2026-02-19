from flask import Flask
from app.database import db


def create_app():
    app = Flask(__name__)

    ## change your_password for your MySQL password
    ## flowcyto_db is the database name by default
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/flowcyto_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'una_clave_super_secreta_123'
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes     ## importamos las rutas aquí para evitar importaciones circulares

    return app

