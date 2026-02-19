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
            # Sumamos todos los 'total_score' 
            suma_total_scores = sum(row.total_score for row in ranking)

            # Convertimos la lista ['CD4', 'CD8'] en un string "CD4, CD8"
            genes_string = ", ".join(lista_genes)
        
            # Creamos la "cabecera" de la búsqueda en la tabla Prediction
            nueva_prediccion = Prediction(user_email=user_email, input_genes=genes_string, request_date=datetime.now())
            db.session.add(nueva_prediccion)
            db.session.flush() # Esto nos da el ID de la predicción sin cerrar la sesión

            # Guardamos cada línea del ranking en la tabla Result
            for row in ranking:

                prob = 0
                if suma_total_scores > 0:
                    prob = (row.total_score / suma_total_scores) * 100

                nuevo_resultado = Result(
                    prediction_id=nueva_prediccion.prediction_id,
                    cell_type_id=row.cell_type_id,
                    score=row.total_score,
                    probability_pct=round(prob, 2) # Redondeamos probabilidad a 2 decimales
                )
                db.session.add(nuevo_resultado)
        
            db.session.commit() # Guardamos todo de golpe en MySQL

        # Calculamos probabilidades para devolver al frontend
        # Usamos float() porque MySQL devuelve tipo Decimal
        suma_total_scores = float(sum(row.total_score for row in ranking))
        resultado_final = []
        for row in ranking:
            score = float(row.total_score)
            prob = round((score / suma_total_scores) * 100, 2) if suma_total_scores > 0 else 0.0
            resultado_final.append({
                'cell_name': row.cell_name,
                'score': round(score, 2),
                'probability': prob
            })

        return resultado_final
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()  # muestra el error completo en la terminal
        print(f"Error en get_cell_ranking: {e}")
        return []