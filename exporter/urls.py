from django.urls import re_path

import webengine.exporter

app_name = "exporter"

urlpatterns = [re_path(r"^(?P<base>.+)/(?P<modules>.+)/$", webengine.exporter.dispatch)]
