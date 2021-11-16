# Do not remove the 'import *', this is what allows this module to provide
# 'handler404' and 'handler500'. We provide django's default handlers. In a
# nutshell, this module inherits django.conf.urls.defaults and redefines
# whatever it wants. We could import the needed bit explicitely, but if newer
# django versions add other handlers, we'll get bit in the a** again. Django's
# API is retarded, but whatever.
# See http://docs.djangoproject.com/en/dev/topics/http/views/#the-404-page-not-found-view

from django.conf.urls import patterns, url, include
from webengine.utils import get_valid_plugins
from django.contrib import admin
from django.conf import settings

# List of patterns to apply, default view is webengine.index
urlpatterns = patterns(
    "",
    url(r"^$", "webengine.utils.default_view"),
)

if hasattr(settings, "ENABLE_ADMIN") and settings.ENABLE_ADMIN:
    admin.autodiscover()
    # List of patterns to apply, default view is webengine.index
    urlpatterns += patterns("", (r"^admin/(.*)$", admin.site.root))

plugs = get_valid_plugins()

for name, mod in plugs:
    # Append patterns of each plugins
    # Let each plugin define their urlpatterns, just concat them here.
    urlpatterns += patterns("", (r"^" + name + "/", include(name + ".urls")))
    # JS translations. We have to prepend 'webengine.' to the package
    # name since it is the way it is spelled in
    # settings.INSTALLED_APPS; see also #2306.
    urlpatterns += patterns(
        "",
        url(
            r"^jsi18n/" + name + "/$",
            "django.views.i18n.javascript_catalog",
            {"packages": ["webengine." + name]},
        ),
    )

# JUST FOR DEBUG PURPOSE, STATIC PAGES WILL BE SERVED BY APACHE.


if settings.DEBUG:
    urlpatterns += patterns(
        "",
        (
            r"^medias/(?P<path>.*)$",
            "django.views.static.serve",
            {"document_root": "/usr/share/webengine/medias/"},
        ),
    )

if hasattr(settings, "ENABLE_ADMIN") and settings.ENABLE_ADMIN:
    urlpatterns += patterns(
        "",
        (
            r"^admin/(?P<path>.*)$",
            "django.views.static.serve",
            {
                "document_root": "/usr/share/python-django-common/django/contrib/admin/static/admin/"
            },
        ),
    )
