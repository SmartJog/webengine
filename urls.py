from django.conf.urls.defaults import *

# URLs here will define which RxtxManager plug-in are enable for this set up.
urlpatterns = patterns('',
        (r'^$', 'rxtxmanager.views.index'),
        (r'^telecommande/', include('telecommande.urls')),
        (r'^automationsws/', include('automations.urls'), {'output': 'json'}),
        (r'^automations/', include('automations.urls')),
)
