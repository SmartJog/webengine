from django.conf import settings
import django.utils.simplejson as json
from django.views.decorators.http import require_POST

from webengine.importer import importer
from webengine.utils.decorators import render

@render
@require_POST
def dispatch(request, *args, **kw):
    """
        Called when a URL created by exporter.urls.create_patterns() match.
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
