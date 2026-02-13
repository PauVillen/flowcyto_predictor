## este script contiene lo que pasa cuando el usuario hace una query:
## 1)recibir el input de los genes del usuario, 2)unirlos con los markers y cell types en una sola consulta (join), y 3)calcular el ranking

from flask import render_template, request, current_app as app
from app.database import db
from app.models import Gene, Marker, CellType, Prediction, Result
from sqlalchemy import func



@app.route('/')
def home():
    return render_template('buscador.html')     ## encara se ha de fer este html :)



@app.route('/buscar', methods=['POST'])
def search():

    ## obtener la query del user y "limpiarla" (splitear la string de genes y crear una lista)
    genes_input = request.form.get('genes_input', '')
    lista_genes = [s.strip().upper() for s in genes_input.split(',') if s.strip()]

    if not lista_genes:      ## falta x hacer el buscador.html
        return render_template('buscador.html', error="The query input must have at least one gene")



    #### ésto hace la query a la base de datos pa generar el ranking sumando los weights de los markers
    
    # ---> unimos CellType con Marker y Gene para filtrar por los genes de la query
    ranking = db.session.query(
        CellType.cell_name,
        func.sum(Marker.weight).label('total_score')
    ).join(Marker, Marker.cell_type_id == CellType.cell_type_id)\
     .join(Gene, Gene.gene_ensembl_id == Marker.gene_ensembl_id)\
     .filter(Gene.gene_symbol.in_(lista_genes))\
     .group_by(CellType.cell_name)\
     .order_by(func.sum(Marker.weight).desc())\
     .all()


    #### muestra los resultados en el buscador
    return render_template('buscador.html', resultados=ranking, genes_buscados=lista_genes)

