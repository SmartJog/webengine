from django.contrib.auth.models import User
from utils.models import UserSetting
import os

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
