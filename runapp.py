import os

from paste.deploy import loadapp
from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get('PORT', '8080'))
    host = '0.0.0.0'
    app = loadapp('config:production.ini', relative_to='.')

    serve(app, host=host, port=port)
