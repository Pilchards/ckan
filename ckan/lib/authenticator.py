# encoding: utf-8
import json
import logging


from zope.interface import implements
from repoze.who.interfaces import IAuthenticator


from ckan.model import User
import ckan.lib.helpers as h
import ckan.authz as authz

log = logging.getLogger(__name__)


class UsernamePasswordAuthenticator(object):
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None

        login = identity['login']
        user = User.by_name(login)

        if user is None:
            log.debug('Login failed - username %r not found', login)
        elif not user.is_active():
            log.debug('Login as %r failed - user isn\'t active', login)
        elif not user.validate_password(identity['password']):
            log.debug('Login as %r failed - password not valid', login)
        else:
            msg = h.get_billing_api("api/RegisterAndSession/login", request_type='post', ckan_user_id=user.id,
                                    ckan_user_name=user.name, role=authz.is_sysadmin(login))
            decoded = json.loads(msg)
            if decoded['msg'] == 'error':
                log.debug('Login as %r failed - Create the login session failed', login)
            elif decoded['msg'] == 'success':
                return user.name
            else:
                log.debug('Login as %r failed - api/RegisterAndSession/login return wrong data', login)
        # else:
        #     return user.name
        return None
