from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import AnonymousUser

class UserSettingMiddleware(object):
    def process_request(self, request):
        from utils.models import UserSetting
        assert hasattr(request, 'user'), "UserSettingMiddleware require to have the AuthenticationMiddleware before."
        if request.user.is_anonymous(): request.__class__.settings = {}
        else: request.__class__.settings = dict(request.user.usersetting_set.all().values_list('key', 'value'))
        return None

class SSLAuthMiddleware(object):
    def process_request(self, request):
        """ Try to authenticate a user based on SSL certificate. """
        if not hasattr(request, 'user'):
            request.user = get_user(request)
            if request.user.is_authenticated():
                return

        user = authenticate() or AnonymousUser()
        if user.is_authenticated():
            request.user = user
            login(request, user)

class BasicAuthMiddleware(object):
    def process_request(self, request):
        """ Try to authenticate user based on Authorization header. """
        import base64

        if not hasattr(request, 'user'):
            request.user = get_user(request)
            if request.user.is_authenticated():
                return

        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, hash = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = hash.strip().decode('base64')
                username, password = auth.split(':', 1)
                user = authenticate(username=username, password=password) or AnonymousUser()
                if user.is_authenticated():
                    request.user = user
                    login(request, user)
