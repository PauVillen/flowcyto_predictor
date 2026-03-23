from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from app import create_app

original_app = create_app()

PREFIX = 'flowcyto'

from flask import Flask
hostedApp = Flask(__name__)
hostedApp.wsgi_app = DispatcherMiddleware(NotFound(), {
    f"/{PREFIX}": original_app
})

app = hostedApp

if __name__ == "__main__":
    app.run()