from django.conf.urls.defaults import *
from django.conf import settings

def create_patterns():
    """
        Create the patterns from the given exportable modules.
        Will associate uri like: ^/<module_name>/<method_name>/<query_string>$
        to the webengine.exporter.dispatch
    """
    urls = []
    # List of exportable modules.
    mods = settings.EXPORT_MODULES
    for mod in mods:
        # Simple check if importable.
        try:
            __import__(mod, {}, {}, [''])
        except ImportError:
            continue
        reg = '^%s/(?P<modules>.+)/$' % mod
        urls.append(url(reg, 'exporter.dispatch', {'base': mod}))
    return patterns('', *urls)

urlpatterns = create_patterns()
