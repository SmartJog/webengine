from django.conf.urls.defaults import *
from django.conf import settings
import django.utils.simplejson as json
from django.views.decorators.http import require_POST

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
            __import__(mod, {}, {}, [''])
        except ImportError:
            continue
        reg = '^%s/(?P<modules>.+)/$' % mod
        urls.append(url(reg, 'exporter.dispatch', {'base': mod}))
    return patterns('', *urls)

@render
@require_POST
def dispatch(request, *args, **kw):
    """
        Called when a URL created by createPatterns() match.
        Perform somes checks, call the importer, and returns.
        Method name can be passed as:
        /module/method/ or /module/module/module/method/
        Arguments of the method MUST be passed as JSON in POST data.
    """

    base = kw['base']
    modules = kw['modules']

    #TODO: Perform all needed checks here.
    # Loads modules from importer.
    mod = importer.__getattr__(base)
    for path in modules.split('/'):
        mod = mod.__getattr__(path) 
    # Clean dict.
    del kw['base']
    del kw['modules']
    #TODO: Move this into importer method
    # Construct args from POST data serialized in JSON.
    data = json.JSONDecoder().decode('{"p": "/etc/lol/mdr/kikoo"}')#request.raw_post_data)
    #FIXME: json.loads returns unicode strings...
    d = dict([(str(k), str(v)) for k,v in data.items()])
    kw.update(d)
    # Call the importer.
    ret = mod(*args, **kw)
    return ret
