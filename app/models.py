## el esquema de nuestra db en sí

from app.database import db     ## aquí importamos el objeto que hemos creado en database.py
from datetime import datetime



class User(db.Model):
    __tablename__ = 'users'
    user_email = db.Column(db.String(95), primary_key=True)
    user_password = db.Column(db.String(255), nullable=False)


class Gene(db.Model):
    __tablename__ = 'genes'
    gene_ensembl_id = db.Column(db.String(45), primary_key=True)
    gene_symbol = db.Column(db.String(20), unique=True)
    gene_full_name = db.Column(db.String(150))


class CellType(db.Model):
    __tablename__ = 'cell_types'
    cell_type_id = db.Column(db.String(45), primary_key=True)
    cell_name = db.Column(db.String(100), nullable=False)
    cell_description = db.Column(db.Text)


class Marker(db.Model):
    __tablename__ = 'markers'
    gene_ensembl_id = db.Column(db.String(45), db.ForeignKey('genes.gene_ensembl_id'), primary_key=True)
    cell_type_id = db.Column(db.String(45), db.ForeignKey('cell_types.cell_type_id'), primary_key=True)
    weight = db.Column(db.Numeric(5, 2))
    source = db.Column(db.String(100))


class Prediction(db.Model):
    __tablename__ = 'predictions'
    prediction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_genes = db.Column(db.Text, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_email = db.Column(db.String(95), db.ForeignKey('users.user_email'))


class Result(db.Model):
    __tablename__ = 'results'
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.prediction_id'), primary_key=True)
    cell_type_id = db.Column(db.String(45), db.ForeignKey('cell_types.cell_type_id'), primary_key=True)
    score = db.Column(db.Numeric(5, 2))
    probability_pct = db.Column(db.Numeric(5, 2))

    