from django.conf.urls.defaults import *

urlpatterns = patterns('', url('^(?P<base>.+)/(?P<modules>.+)/$', 'exporter.dispatch'))
