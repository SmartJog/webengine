from django.conf.urls.defaults import *
from webengine.utils import get_valid_plugins

# List of patterns to apply, default view is webengine.index
urlpatterns = patterns('',
    url(r'^$', 'webengine.utils.default_view'),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog', name='js_catalog'),
)

plugs = get_valid_plugins()

for name, mod in plugs:
    # Append patterns of each plugins
    # Let each plugin define their urlpatterns, just concat them here.
    urlpatterns += patterns('', (r'^' + name + '/', include(name + '.urls')))

# JUST FOR DEBUG PURPOSE, STATIC PAGES WILL BE SERVED BY APACHE.

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/share/webengine/medias/'}),
    )
