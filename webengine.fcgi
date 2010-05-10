#!/usr/bin/python
import sys, os

sys.path.insert(0, "/usr/share/webengine/app/")
os.chdir("/usr/share/webengine/app/webengine/")
os.environ['DJANGO_SETTINGS_MODULE'] = "webengine.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
