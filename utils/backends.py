from django.contrib.auth.models import User
from utils.models import UserSetting
import os

import settings

from webengine.utils.log import logger

class SSLAuthBackend(object):
    """ Authenticate using SSL certificate. """
    def authenticate(self):
        # No https, no chocolate.
        if os.environ.get('HTTPS', '') != 'on': return None
        try:
            setting = UserSetting.objects.get(key = 'cert_serial', value = os.environ.get('SSL_CLIENT_M_SERIAL', None))
            return setting.user
        except:
            return None
        return None

    def get_user(self, id):
        """ Simply return the user. """
        try:
            return User.objects.get(id = id)
        except User.DoestNotExist:
            return None

class GenericSSLAuthBackend(SSLAuthBackend):
    """ Authenticate using SSL certificate. """
    def authenticate(self):
        # No https, no chocolate.
        if os.environ.get('HTTPS', '') != 'on': return None
        try:
            serial = os.environ.get('SSL_CLIENT_M_SERIAL', None)
            if not serial:
                return None

            mod     = __import__(settings.GENERIC_SSL_AUTH_MODULE)
            model   = getattr(mod.models, settings.GENERIC_SSL_AUTH_MODEL)
            entries = model.objects.filter(**{settings.GENERIC_SSL_AUTH_SERIAL_COLUMN : serial})
            if not entries:
                return None
            for entry in entries:
                return getattr(entry, settings.GENERIC_SSL_AUTH_USER_COLUMN)
            return None
        except:
            return None
        return None
