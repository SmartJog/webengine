from django.contrib import admin
from utils.models import *
from django.contrib import contenttypes
from django.contrib import auth

class UserSettingAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserSetting, UserSettingAdmin)

class ContentTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(contenttypes.models.ContentType, ContentTypeAdmin)

class PermissionAdmin(admin.ModelAdmin):
    pass
admin.site.register(auth.models.Permission, PermissionAdmin)
