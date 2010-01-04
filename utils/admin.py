from django.contrib import admin
from utils.models import *

class UserSettingAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserSetting, UserSettingAdmin)
