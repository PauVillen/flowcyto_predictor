from flask import Flask
from app.database import db


def create_app():
    app = Flask(__name__)

    ## flowcyto_db is the database name by default
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flowcyto_usr:contrasenya_segura_123@localhost/flowcyto_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'una_clave_super_secreta_123'
    
    db.init_app(app)
    
    
    with app.app_context():
        from . import routes     ## import routes here to avoid circular imports

    return app

