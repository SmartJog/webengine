from django.conf.urls.defaults import *

# URLs here will define which RxtxManager plug-in are enable for this set up.
urlpatterns = patterns('',
        (r'^$', 'index.views.index', {'output': 'xml'}),
        (r'^telecommande/', include('telecommande.urls')),
        (r'^automations/', include('automations.urls'), {'output': 'json'}),
)
