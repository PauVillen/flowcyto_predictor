
## LEED LO DE DEBAJO

from flask import Flask
from app.database import db


def create_app():
    app = Flask(__name__)
    
    ## ----> AQUÍ DEBAJO ("tu_password" y "tu_db_name")LO VERDE CADA UNO TIENE Q EDITARLO Y PONER SU OCNTRASEÑA DEL MYSQL Y EL NOMBRE DE LA BASE DE DATOS ("mydb" por defectpo)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:tu_password@localhost/tu_db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes     ## importamos las rutas aquí para evitar importaciones circulares
        
    return app