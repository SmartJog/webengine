from django.contrib import auth
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured


import logging
import traceback


class UserSettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):

        assert hasattr(request, "user"), (
            "UserSettingMiddleware require to have the AuthenticationMiddleware before."
        )
        if request.user.is_anonymous:
            request.__class__.settings = {}
        else:
            request.__class__.settings = dict(
                request.user.usersetting_set.all().values_list("key", "value")
            )


class SSLAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        """Try to authenticate a user based on SSL certificate."""
        if not hasattr(request, "user"):
            request.user = get_user(request)
            if request.user.is_authenticated:
                return

        user = authenticate() or AnonymousUser()
        if user.is_authenticated:
            request.user = user
            login(request, user)


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        """Try to authenticate user based on Authorization header."""

        if not hasattr(request, "user"):
            request.user = get_user(request)
            if request.user.is_authenticated:
                return

        if "HTTP_AUTHORIZATION" in request.META:
            authmeth, hash = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
            if authmeth.lower() == "basic":
                auth_string = hash.strip().decode("base64")
                username, password = auth_string.split(":", 1)
                user = (
                    authenticate(username=username, password=password)
                    or AnonymousUser()
                )
                if user.is_authenticated:
                    request.user = user
                    login(request, user)


class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger = logging.getLogger("webengine.utils.exceptions")
        logger.error(traceback.format_exc())
        return None


class RemoteUserMiddleware:
    """
    Middleware for utilizing web-server-provided authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.

    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class."
            )
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.username == self.clean_username(username, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username
