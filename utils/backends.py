from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import UserSetting
import os

import settings

from webengine.utils.log import logger


class SSLAuthBackend:
    """Authenticate using SSL certificate."""

    def authenticate(self):
        # No https, no chocolate.
        if os.environ.get("HTTPS", "") != "on":
            return None
        try:
            setting = UserSetting.objects.get(
                key="cert_serial", value=os.environ.get("SSL_CLIENT_M_SERIAL", None)
            )
            return setting.user
        except:
            return None
        return None

    def get_user(self, id):
        """Simply return the user."""
        try:
            return User.objects.get(id=id)
        except User.DoestNotExist:
            return None


class GenericSSLAuthBackend(SSLAuthBackend):
    """Authenticate using SSL certificate."""

    def authenticate(self):
        # No https, no chocolate.
        if os.environ.get("HTTPS", "") != "on":
            return None
        try:
            serial = os.environ.get("SSL_CLIENT_M_SERIAL", None)
            if not serial:
                return None

            mod = __import__(settings.GENERIC_SSL_AUTH_MODULE)
            model = getattr(mod.models, settings.GENERIC_SSL_AUTH_MODEL)
            entries = model.objects.filter(
                **{settings.GENERIC_SSL_AUTH_SERIAL_COLUMN: serial}
            )
            if not entries:
                return None
            for entry in entries:
                return getattr(entry, settings.GENERIC_SSL_AUTH_USER_COLUMN)
            return None
        except:
            return None
        return None


class RemoteUserBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, remote_user):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
        return user

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        By default, returns the username unchanged.
        """
        return username

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        return user
