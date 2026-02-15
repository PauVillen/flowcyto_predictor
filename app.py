## es el lanzador de la app  (no hay q tocar nada de aquí)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 