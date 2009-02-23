from django.conf.urls.defaults import *
from django.conf import settings

from webengine.importer import importer
from webengine.utils.decorators import render

def createPatterns():
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
            __import__(mod, {}, {}, {})
        except ImportError:
            print 'gaoule'
            continue
        reg = '^%s/(?P<modules>.+)/$' % mod
        print reg
        urls.append(url(reg, 'exporter.dispatch', {'base': mod}))
    return patterns('', *urls)

@render
def dispatch(request, *args, **kw):
    """
        Called by the URL dispatcher.
        Perform somes checks, call the importer, and returns.
        Arguments can be:
        /module/method/ or /module/module/module/method/
    """

    base = kw['base']
    modules = kw['modules']

    #TODO: Perform all needed checks here.
    mod = importer.__getattr__(base)
    for path in modules.split('/'):
        mod = mod.__getattr__(path) 
    return mod(*args, **kw)
