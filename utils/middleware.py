class UserSettingMiddleware(object):
    def process_request(self, request):
        from utils.models import UserSetting
        assert hasattr(request, 'user'), "UserSettingMiddleware require to have the AuthenticationMiddleware before."
        if request.user.is_anonymous(): request.__class__.settings = {}
        else: request.__class__.settings = dict(UserSetting.objects.filter(user = request.user).values_list('key', 'value'))
        return None

