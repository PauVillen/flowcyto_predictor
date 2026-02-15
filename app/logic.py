# app/logic.py
from datetime import datetime
from sqlalchemy import func
from app.database import db
from app.models import CellType, Marker, Gene, Prediction, Result

def get_cell_ranking(lista_genes, user_email=None):
    """
    Recibe una lista de genes y devuelve el ranking de células 
    calculado desde la base de datos.
    """
    
    if not lista_genes:
        return []
        
    try:
        ranking = db.session.query(
            CellType.cell_type_id, # for storing in results
            CellType.cell_name,
            func.sum(Marker.weight).label('total_score')
        ).join(Marker, Marker.cell_type_id == CellType.cell_type_id)\
        .join(Gene, Gene.gene_ensembl_id == Marker.gene_ensembl_id)\
        .filter(Gene.gene_symbol.in_(lista_genes))\
        .group_by(CellType.cell_type_id, CellType.cell_name)\
        .order_by(func.sum(Marker.weight).desc())\
        .all()
        
        # Si hay resultados y tenemos un usuario, guardamos en la DB
        if ranking and user_email:
            # Convertimos la lista ['CD4', 'CD8'] en un string "CD4, CD8"
            genes_string = ", ".join(lista_genes)
        
            # Creamos la "cabecera" de la búsqueda en la tabla Prediction
            nueva_prediccion = Prediction(user_email=user_email, input_genes=genes_string, request_date=datetime.now())
            db.session.add(nueva_prediccion)
            db.session.flush() # Esto nos da el ID de la predicción sin cerrar la sesión

            # Guardamos cada línea del ranking en la tabla Result
            for row in ranking:
                nuevo_resultado = Result(
                    prediction_id=nueva_prediccion.prediction_id,
                    cell_type_id=row.cell_type_id,
                    score=row.total_score,
                    probability_pct=None # De momento no calculamos %
                )
                db.session.add(nuevo_resultado)
        
            db.session.commit() # Guardamos todo de golpe en MySQL
    
        return ranking
    
    except Exception as e:
        db.session.rollback() # Importante: si algo falla, deshacemos los cambios
        # Si hay un error de conexión o de SQL, lo imprimimos para saber qué pasa
        print(f"Error en la consulta de ranking: {e}")
        return []
