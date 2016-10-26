from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
    Allow,
)

from ..models.models import DBSession, UserAccount


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.userid

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user is not None:
            principals.append(Authenticated)
            principals.append(str(user.userid))
            principals.append('role:' + user.role)
        return principals

def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = DBSession.query(UserAccount).get(user_id)
        return user

def groupfinder(userid, request):
    user = UserAccount.by_id(userid)
    return user.role

def includeme(config):
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
        'sosecert',
        hashalg='sha512',
        callback = groupfinder,
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)

class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'role:editors', ('editor')),
               (Allow, Authenticated, 'viewprofile')]
    def __init__(self, request):
        pass
