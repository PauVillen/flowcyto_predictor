# app/routes.py

from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from app.database import db
from app.models import User, Prediction, Result, CellType
from app.logic import get_cell_ranking

@app.route('/')
def home():
    return render_template('index.html')   # ← siempre muestra el home


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscamos al usuario en la base de datos
        user = User.query.filter_by(user_email=email, user_password=password).first()
        
        if user:
            session['user_email'] = user.user_email # Guardamos el email en la sesión
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        # Nota: Aquí falta la función es_email_valido si no está definida arriba, 
        # pero he mantenido tu lógica original del archivo adjunto
        password = request.form.get('password')
        
        # Comprobar si el usuario ya existe
        user = User.query.filter_by(user_email=email).first()
        if user:
            return render_template('register.html', error="Already existing email.")

        # Crear el nuevo usuario
        new_user = User(user_email=email, user_password=password)
        
        # Guardar en la base de datos
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) # Si sale bien, al login
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', error="Error in register.")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear() # Borramos la sesión
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'], endpoint='search') # Añadimos endpoint='search'
def search():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    # 1. Obtener los genes del formulario
    genes_raw = request.form.get('genes_input')

    # CORRECCIÓN AQUÍ: Validamos que genes_raw no sea None antes de hacer split
    if not genes_raw or genes_raw.strip() == "":
        flash("Por favor, introduce al menos un gen para realizar la búsqueda.", "warning")
        return render_template('buscador.html')

    # 2. Limpiar la lista de genes
    genes_input = genes_raw.split(',')
    lista_genes = [g.strip().upper() for g in genes_input if g.strip()]

    # 3. Llamar a la lógica que calcula el ranking
    # Aquí es donde realmente se obtienen los datos de la DB
    ranking = get_cell_ranking(lista_genes, user_email=user_email)

    # 4. Verificar si hay resultados
    if not ranking:
        flash("No se encontraron resultados para los genes introducidos.", "info")
        return render_template('buscador.html', genes_buscados=lista_genes)

    # 5. Enviar resultados al HTML
    # Importante: resultados=ranking para que tu HTML lo reconozca
    return render_template('buscador.html', resultados=ranking, genes_buscados=lista_genes)

@app.route('/profile')
def profile():
    user_email = session.get('user_email')
    
    # Si no ha iniciado sesión , lo mandamos al login
    if not user_email:
        return redirect(url_for('login'))

    # 1. Buscar todas las predicciones de este usuario (ordenadas de más nueva a más antigua)
    predictions = Prediction.query.filter_by(user_email=user_email).order_by(Prediction.request_date.desc()).all()

    # 2. Construir una lista con la información estructurada
    history = []
    for pred in predictions:
        # Por cada predicción, buscamos sus mejores 5 resultados
        results = db.session.query(Result, CellType.cell_name)\
            .join(CellType, Result.cell_type_id == CellType.cell_type_id)\
            .filter(Result.prediction_id == pred.prediction_id)\
            .order_by(Result.probability_pct.desc())\
            .limit(5).all()

        # Damos formato a la fecha 
        date_str = pred.request_date.strftime("%d-%m-%Y %H:%M") if pred.request_date else "Sin fecha"

        history.append({
            'date': date_str,
            'genes': pred.input_genes,
            'results': results
        })

    return render_template('profile.html', user_email=user_email, history=history)