# app/routes.py

from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from app.database import db
from sqlalchemy import func
from app.models import User, Prediction, Result, CellType, Marker, Gene
from app.logic import get_cell_ranking

@app.route('/')
def home():
    return render_template('index.html')   # always show home


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Search for user in database
        user = User.query.filter_by(user_email=email, user_password=password).first()
        
        if user:
            session['user_email'] = user.user_email # Save the email in the session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
       
        password = request.form.get('password')
        
        # Check if user already exists
        user = User.query.filter_by(user_email=email).first()
        if user:
            return render_template('register.html', error="Already existing email.")

        # Create new user
        new_user = User(user_email=email, user_password=password)
        
        # Save in database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) # Go to login if register successful
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', error="Error in register.")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear() # Erase session
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'], endpoint='search') # Add endpoint='search'
def search():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    # 1. Obtain gains from form
    genes_raw = request.form.get('genes_input')
    # Validate genes_raw is not None before splitting
    if not genes_raw or genes_raw.strip() == "":
        flash("Please, introduce at least one gene to perform the search.", "warning")
        return render_template('buscador.html')

    # 2. Clean gene list
    genes_input = genes_raw.split(',')
    lista_genes = [g.strip().upper() for g in genes_input if g.strip()]

    # 3. Call the logic to calculate the ranking
    ranking = get_cell_ranking(lista_genes, user_email=user_email)

    # 4. Check if there are results
    if not ranking:
        flash("No results found for the input genes.", "info")
        return render_template('buscador.html', genes_buscados=lista_genes)

    # 5. Send results to HTML
    return render_template('buscador.html', resultados=ranking, genes_buscados=lista_genes)

@app.route('/profile')
def profile():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    # 1. Look for user predictions
    predictions = Prediction.query.filter_by(user_email=user_email).order_by(Prediction.request_date.desc()).all()

    history = []
    for pred in predictions:
        lista_genes = [g.strip().upper() for g in pred.input_genes.split(',')]

        # 2. Results
        results = db.session.query(
            Result.score,
            Result.probability_pct,
            CellType.cell_name,
            CellType.cell_description,
            func.group_concat(Marker.source.distinct()).label('sources')
        ).join(CellType, Result.cell_type_id == CellType.cell_type_id)\
         .join(Marker, Marker.cell_type_id == CellType.cell_type_id)\
         .join(Gene, Gene.gene_ensembl_id == Marker.gene_ensembl_id)\
         .filter(Result.prediction_id == pred.prediction_id)\
         .filter(Gene.gene_symbol.in_(lista_genes))\
         .group_by(Result.score, Result.probability_pct, CellType.cell_name, CellType.cell_description)\
         .order_by(Result.probability_pct.desc())\
         .limit(5).all()

        date_str = pred.request_date.strftime("%Y-%m-%d %H:%M") if pred.request_date else "Sin fecha"

        history.append({
            'date': date_str,
            'genes': pred.input_genes,
            'results': results
        })

    return render_template('profile.html', user_email=user_email, history=history)