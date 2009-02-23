from django.conf.urls.defaults import *
from webengine.exporter import createPatterns

# URLs here will define which RxtxManager plug-in are enable for this set up.
urlpatterns = patterns('',
        (r'^$', 'rxtxmanager.views.index'),
        (r'^telecommande/', include('telecommande.urls')),
        (r'^automations/', include('automations.urls')),
)

# Add exporter module's urls.
urlpatterns += createPatterns()
