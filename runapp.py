import os

from paste.deploy import loadapp
from waitress import serve
import bin

if __name__ == "__main__":
    port = int(os.environ.get('PORT', '8080'))
    host = '0.0.0.0'

    settings = {}
    settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    settings['pyramid.includes'] = ['pyramid_tm']

    serve(bin.main({}, **settings), host=host, port=port)
