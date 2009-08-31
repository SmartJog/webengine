from django.conf.urls.defaults import *
from webengine.utils import get_valid_plugins

# List of patterns to apply, default view is webengine.index
urlpatterns = patterns('',
    url(r'^$', 'webengine.utils.default_view'),
)

plugs = get_valid_plugins()

for name, mod in plugs:
    # Append patterns of each plugins
    # Let each plugin define their urlpatterns, just concat them here.
    urlpatterns += patterns('', (r'^' + name + '/', include(name + '.urls')))
    # JS translations. We have to prepend 'webengine.' to the package
    # name since it is the way it is spelled in
    # settings.INSTALLED_APPS; see also #2306.
    urlpatterns += patterns('', url(r'^jsi18n/' + name + '/$', 'django.views.i18n.javascript_catalog', {'packages': ['webengine.' + name]}))


# JUST FOR DEBUG PURPOSE, STATIC PAGES WILL BE SERVED BY APACHE.

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/share/webengine/medias/'}),
    )
