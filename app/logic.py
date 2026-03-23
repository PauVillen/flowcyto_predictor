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
            CellType.cell_type_id,
            CellType.cell_name,
            CellType.cell_description, 
            func.group_concat(Marker.source.distinct()).label('sources'), 
            func.sum(Marker.weight).label('total_score')
        ).join(Marker, Marker.cell_type_id == CellType.cell_type_id)\
        .join(Gene, Gene.gene_ensembl_id == Marker.gene_ensembl_id)\
        .filter(Gene.gene_symbol.in_(lista_genes))\
        .group_by(CellType.cell_type_id, CellType.cell_name, CellType.cell_description)\
        .order_by(func.sum(Marker.weight).desc())\
        .all()
        
        # If there are results and user, save in DB
        if ranking and user_email:
            # Add all the 'total_score' 
            suma_total_scores = sum(row.total_score for row in ranking)

            # Convert the list to string
            genes_string = ", ".join(lista_genes)
        
            # Create search header in Prediction table
            nueva_prediccion = Prediction(user_email=user_email, input_genes=genes_string, request_date=datetime.now())
            db.session.add(nueva_prediccion)
            db.session.flush() # Gives us the prediction ID without closing session

            # Save each line of ranking in Results table
            for row in ranking:

                prob = 0
                if suma_total_scores > 0:
                    prob = (row.total_score / suma_total_scores) * 100

                nuevo_resultado = Result(
                    prediction_id=nueva_prediccion.prediction_id,
                    cell_type_id=row.cell_type_id,
                    score=row.total_score,
                    probability_pct=round(prob, 2) # Round probability to 2 decimals
                )
                db.session.add(nuevo_resultado)
        
            db.session.commit() # Save all in MySQL

        # Calculate probabilities
        suma_total_scores = float(sum(row.total_score for row in ranking))
        resultado_final = []
        for row in ranking:
            score = float(row.total_score)
            prob = round((score / suma_total_scores) * 100, 2) if suma_total_scores > 0 else 0.0
            resultado_final.append({
                'cell_name': row.cell_name,
                'description': row.cell_description, 
                'sources': row.sources,              
                'score': round(score, 2),
                'probability': prob
            })

        return resultado_final
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()  # show the complete error in terminal
        print(f"Error en get_cell_ranking: {e}")
        return []