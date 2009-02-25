from django.conf.urls.defaults import *
from webengine.utils import get_valid_plugins

# List of patterns to apply, default view is webengine.index
urlpatterns = patterns('', (r'^$', 'webengine.index'))

plugs = get_valid_plugins()

for name, mod in plugs:
    # Append patterns of each plugins
    # Let each plugin define their urlpatterns, just concat them here.
    print name
    # Special case for exporter.
    if name == 'exporter': urlpatterns += mod.urls.urlpatterns
    else: urlpatterns += patterns('', (r'^' + name + '/', include(name + '.urls')))
