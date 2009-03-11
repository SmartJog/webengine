# Utils.py
# Some tools.

from django.http import HttpResponse
from django.conf import settings
from django import http

from webengine.utils.exceptions import *

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
        self.decorator_opts = kwds
        self.func = func
        self.__name__ = '_CheckRenderMode'
        # Default values
        self.output = settings.DEFAULT_OUTPUT_MODE
        self.view = None
        self.status = 200
        self.view_ctx = {}

    def __call__(self, request, *args, **kwds_urldispatcher):
        """
            Check are done in this order, each mode found override the previous.
            - Default from settings.DEFAULT_OUTPUT_MODE
            - Header from request. (FIXME: which header field?)
            - 'output' passed by the urldispatcher (which is passed to every controller methods).
            - Forced 'output' passed in the decorator's dictionary.
            View name can be defined by several ways (override the previous).
            - 'view' key passed by the urldispatcher.
            - Passed in the decorator's dictionary.
            - 'view' key in the returned dictionary.
            The __call__() is responsible of the outputed data.
            This method is called by the urldispatcher method from Django.
        """
        self.status = 200
        self.request = request
        # Header (Change this, send by every browser)
        # if request.META['HTTP_ACCEPT']: mode = _extract_type(request.META['HTTP_ACCEPT'])
        # Check for keyword passed by the url dispatcher.
        self.output = settings.DEFAULT_OUTPUT_MODE
        self.output = kwds_urldispatcher.pop('output', self.output)
        # Check forced output by decorator.
        if 'output' in self.decorator_opts.keys(): self.output = self.decorator_opts['output']
        # Check output validity, otherwise raise 500.
        if self.output not in settings.ACCEPTABLE_OUTPUT_MODES.keys(): return HttpResponse(status = 500)
        # Lookup the right view.
        # Passed by the urldispatcher
        self.view = kwds_urldispatcher.get('view', None)
        # The view method. FIXME: Catch exceptions ?
        ret = self.func(request, *args, **kwds_urldispatcher)
        # Check return type.
        # The view method generate no output, just return an empty HttpResponse.
        if ret is None: return HttpResponse()
        self.view_ctx = ret
        # Got tuple? (status, {dict})
        if isinstance(ret, tuple):
            self.status = ret[0]
            self.view_ctx = ret[1]
        # Got a HttpResponse ? Return.
        elif isinstance(ret, HttpResponse): return ret
        # Check for view into the decorator's dictionary.
        self.view = self.decorator_opts.get('view', self.view)
        # Check for view into the returned dictionary.
        if isinstance(ret, dict) and 'view' in self.view_ctx.keys():
            self.view = self.view_ctx.pop('view')
        return self._createResponse()

    def _createResponse(self):
        from django.template import loader, RequestContext, TemplateDoesNotExist
        import inspect

        # View is None, check for a Factory for this output mode.
        if self.view is None:
            from webengine.utils.generators import GeneratorFactory
            generator = GeneratorFactory.get(self.output)
            ret = generator.generate(self.view_ctx)
            if ret is None: raise ImpossibleRenderingException("Unable to render.")
            # Generators returns a string, wrap it within a HttpResponse.
            return HttpResponse(ret,
                                content_type = settings.ACCEPTABLE_OUTPUT_MODES[self.output],
                                status = self.status)
        # Append the output mode to the view.
        self.view += '.' + self.output
        # Extract module name, concat with templates dir and create final view name
        mod = inspect.getmodule(self.func).__name__
        i = mod.rfind('.')
        module, attr = mod[:i], mod[i+1:]
        self.view = '/'.join([module, self.view])
        try:
            from webengine.utils import webengine_template_processor

            template = loader.get_template(self.view)
            ctx = RequestContext(self.request, self.view_ctx, [webengine_template_processor])
            resp = HttpResponse(template.render(ctx),
                                content_type = settings.ACCEPTABLE_OUTPUT_MODES[self.output],
                                status = self.status)
            return resp
        except TemplateDoesNotExist, e:
            #TODO: Fallback to a "raw" output.
            #return HttpResponse('Template does not exist', status = 500)
            raise

""" DECORATORS """
def render(function=None, **kwds):
    """ This decorator MUST wrap any controller methods. """
    if function: return _CheckRenderMode(function, **kwds)
    def __nested__(func):
        return _CheckRenderMode(func, **kwds)
    return __nested__
