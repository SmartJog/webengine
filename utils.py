# Utils.py
# Some tools.

from django.http import HttpResponse
from django.conf import settings

class _CheckRenderMode(object):
    """
        Callable object that will act like a decorator.
        Wraps calls to view methods.
        Determine which kind of output to perform, based on (in this order):
            * Default setting output mode (which variable?).
            * HTTP Header (which one?).
            * 'output' passed by the urldispatcher.
            * "Forced" 'output' passed in the decorator's dictionary.
        The priority is descending, the last one is the strongest.
    """
    def __init__(self, func, **kwds):
        self.keywords = kwds
        self.func = func
        self.func_name = func.__name__
        self.view = kwds.get('view', '')

    def __call__(self, request, *args, **kwds):
        """
            Check are done in this order, each mode found override the previous.
            - Default from settings.DEFAULT_OUTPUT_MODE
            - Header from request. (FIXME: which header field?)
            - 'output' passed by the urldispatcher (which is passed to every controller methods).
            - Forced 'output' passed in the decorator's dictionary.
            The __call__() is responsible of the outputed data.
        """
        # Get from configuration
        output = settings.DEFAULT_OUTPUT_MODE
        # Header (Change this, send by every browser)
        # if request.META['HTTP_ACCEPT']: mode = _extract_type(request.META['HTTP_ACCEPT'])
        # Check for keyword passed by the url dispatcher.
        if 'output' in kwds:
            output = kwds['output']
            del kwds['output']
        # Check forced output by decorator.
        if 'output' in self.keywords.keys(): output = self.keywords['output']
        # Lookup the right view.
        view = None
        # Passed in the decorator dict?
        if 'view' in kwds:
            view = kwds['view'] #Add right extension
            del kwds['view']
        # The view method.
        ret = self.func(request, *args, **kwds)
        # Check return type.
        status = 200
        dict = ret
        # Got tuple? (status, {dict})
        if type(ret).__name__ == 'tuple':
            status = ret[0]
            dict = ret[1]
        # Got anything but a dict? Return, don't handle this request.
        elif type(ret).__name__ != 'dict': return ret # Not a dict
        # Create the response, using the right view depending on the output mode.
        return HttpResponse("Je suis une requete, mon mode de rendu est " + output + ", status=" + str(status) + " view: " + str(view))

"""
    DECORATORS
"""
def render(function=None, **kwds):
    """
        This decorator MUST wrap any controller methods.
    """
    if function: return _CheckRenderMode(function, **kwds)
    def __nested__(func):
        return _CheckRenderMode(func, **kwds)
    return __nested__
