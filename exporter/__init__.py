import django.utils.simplejson as json
from django.http import HttpResponse

from webengine.importer import importer
from webengine.utils.decorators import render

@render
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
    ret = None
    if request.method == "GET":
        # GET method, no args, return directly the result
        ret = mod()
    elif request.method == "POST":
        #TODO: Move this into importer method
        # Construct args from POST data serialized in JSON.
        data = json.JSONDecoder().decode('{"p": "/etc/lol/mdr/kikoo"}')#request.raw_post_data)
        #FIXME: json.loads returns unicode strings...
        d = dict([(str(k), str(v)) for k,v in data.items()])
        kw.update(d)
        # Call the importer.
        ret = mod(*args, **kw)
    else: return HttpResponse('Method not supported', status = 405)

    return HttpResponse(ret)
