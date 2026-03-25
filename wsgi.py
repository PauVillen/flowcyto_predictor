from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from app import create_app
from flask import Flask

original_app = create_app()
PREFIX = 'flowcyto'

hostedApp = Flask(__name__)
hostedApp.wsgi_app = DispatcherMiddleware(NotFound(), {
    f"/{PREFIX}": original_app
})

def proxy_fix_app(environ, start_response):
    environ['HTTP_HOST'] = 'formacio.bq.ub.edu'
    environ['wsgi.url_scheme'] = 'https'
    return hostedApp(environ, start_response)

app = proxy_fix_app