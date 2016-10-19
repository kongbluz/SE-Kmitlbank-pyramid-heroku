from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import sys
<<<<<<< HEAD
from os import getcwd

sys.path.append(getcwd() + "\\models")
from models  import DBSession, Base
=======
sys.path.append(getcwd() + "\\models")
from models.models  import DBSession, Base
>>>>>>> cbf2404d2a088a65816edf2cee55b6e87f74a835

def main(global_config, **settings):

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings = settings)
    config.include('pyramid_chameleon')
    config.include('.securitys.security')
    config.include('.route')
    config.scan()
    return config.make_wsgi_app()
