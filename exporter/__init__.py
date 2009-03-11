import simplejson as json
from webengine.importer import importer
from webengine.importer import ImporterError
from webengine.utils.decorators import render
from webengine.utils.log import logger

@render(output='json')
def dispatch(request, *args, **kw):
    """
        Called when a URL created by exporter.urls.create_patterns() match.
        Perform somes checks, call the importer, and returns.
        Method name can be passed as:
        /module/method/ or /module/module/module/method/
        Arguments of the method MUST be passed as JSON in POST data.

        This method is not meant to be called directly with a web browser.
    """

    base = kw.pop('base')
    modules = kw.pop('modules')

    #TODO: Limit access to some parts of the API.
    #TODO: Perform all needed checks here.
    # Loads modules from importer.
    importer.set_request(request)
    mod = importer.__getattr__(base)
    for path in modules.split('/'):
        mod = mod.__getattr__(path)
    # Call the importer, and return directly to let the render
    # decorator decide how to render it.
    try:
        ret = mod(*args, **kw)
        return (200, ret)
    except ImporterError, e:
        logger.debug("Exporter: Catched   : " + e.msg)
        logger.debug("Exporter: Traceback : " + e.traceback)
        return (500, {'msg': e.msg, 'traceback': e.traceback})
