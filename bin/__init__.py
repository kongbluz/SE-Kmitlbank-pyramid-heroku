from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from /models.models  import DBSession, Base

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
