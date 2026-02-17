# app/routes.py

from flask import render_template, request, redirect, url_for, session, flash, current_app as app
from app.database import db
from app.models import User
from app.logic import get_cell_ranking

@app.route('/')
def home():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('buscador.html')

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

@app.route('/search', methods=['POST'])
def search():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    ## obtener query del user y "limpiarla" (split string of genes & create list)
    genes_input = request.form.get('genes_input', '')
    lista_genes = [s.strip().upper() for s in genes_input.split(',') if s.strip()]

    if not lista_genes:      
        return render_template('buscador.html', error="The query input must have at least one gene")

    ranking = get_cell_ranking(lista_genes, user_email=user_email)
    return render_template('buscador.html', resultados=ranking, genes_buscados=lista_genes)

