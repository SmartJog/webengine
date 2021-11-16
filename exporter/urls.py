from django.conf.urls import patterns, url

urlpatterns = patterns("", url("^(?P<base>.+)/(?P<modules>.+)/$", "exporter.dispatch"))
