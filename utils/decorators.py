# Utils.py
# Some tools.

from django.http import HttpResponse
from django.conf import settings
from django import http

from webengine.utils.exceptions import *
from webengine import settings

import importer

class _CheckRenderMode(object):
    """
        Callable object that will act like a decorator.
        Wraps calls to view methods.
        Determine which kind of output to perform, based on (in this order):
            * Default setting output mode (which variable?).
            * 'output' passed by the urldispatcher.
            * "Forced" 'output' passed in the decorator's dictionary.
            * HTTP Header: WEBENGINE_OUTPUT.
        The priority is descending, the last one is the strongest.
    """
    def __init__(self, func, **kwds):
        import inspect

        self.decorator_opts = kwds
        self.func = func
        # Extract func's module name
        mod = inspect.getmodule(self.func).__name__
        i = mod.rfind('.')
        if i == -1: self.func_mod_name = mod
        else: self.func_mod_name, attr = mod[:i], mod[i+1:]
        self.__name__ = '_CheckRenderMode'
        # Default values
        self.input = settings.DEFAULT_INPUT_MODE
        self.output = settings.DEFAULT_OUTPUT_MODE
        self.view = None
        self.status = 200
        self.view_ctx = {}

    def __call__(self, request, *args, **kwds_urldispatcher):
        """
            Check are done in this order, each mode found override the previous.
            - Default from settings.DEFAULT_OUTPUT_MODE
            - 'output' passed by the urldispatcher (which is passed to every controller methods).
            - Forced 'output' passed in the decorator's dictionary.
            - Header from request: WEBENGINE_OUTPUT
            View name can be defined by several ways (override the previous).
            - 'view' key passed by the urldispatcher.
            - Passed in the decorator's dictionary.
            - 'view' key in the returned dictionary.
            The __call__() is responsible of the outputed data.
            This method is called by the urldispatcher method from Django.
        """
        self.status = 200
        self.request = request
        # Check for input in the content-type header
        ct_value = request.META['CONTENT_TYPE'] or settings.DEFAULT_INPUT_MODE
        ct_value = ct_value.split(';')[0]
        if ct_value in settings.ACCEPTABLE_INPUT_MODES:
            self.input = settings.ACCEPTABLE_INPUT_MODES[ct_value]
        else:
            self.input = settings.DEFAULT_INPUT_MODE
        # Check forced input by decorator.
        if 'input' in self.decorator_opts.keys(): self.input = self.decorator_opts['input']
        # Decode input
        from webengine.utils.decoders import DecoderFactory
        decoder = DecoderFactory.get(self.input)
        if request.method == 'POST':
            request.DECODED = decoder.decode(request.raw_post_data)
        else:
            request.DECODED = None
        # Check for output keyword passed by the url dispatcher.
        self.output = settings.DEFAULT_OUTPUT_MODE
        self.output = kwds_urldispatcher.pop('output', self.output)
        # Check forced output by decorator.
        if 'output' in self.decorator_opts.keys(): self.output = self.decorator_opts['output']
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
        if isinstance(self.view_ctx, dict):
            # Check for view into the returned dictionary.
            if 'view' in self.view_ctx.keys(): self.view = self.view_ctx.pop('view')
            # Output from returned dictionary.
            if 'output' in self.view_ctx.keys(): self.output = self.view_ctx.pop('output')
        # Header (override everything)
        if self.request.META.get('HTTP_WEBENGINE_OUTPUT'): self.output = request.META['HTTP_WEBENGINE_OUTPUT']
        # Check output validity, otherwise raise 500.
        if self.output not in settings.ACCEPTABLE_OUTPUT_MODES.keys(): return HttpResponse(status = 500)
        return self._createResponse()

    def _createResponse(self):
        from django.template import loader, RequestContext, TemplateDoesNotExist

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
        self.view = '/'.join([self.func_mod_name, self.view])
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

class _Export(object):
    """ Set a member "__exportable__" which will be checked
    by Importer, to decide if "request" parameter must be given. """
    def __init__(self, func):
        self.__exportable__ = True
        self.__func__ = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__dict__.update(func.__dict__)

    def __call__(self, request, *args, **kw):

        return self.__func__(request, *args, **kw)

class _Proxy(object):
    """ Set a member "__exportable__" which will be checked
    by Importer, to decide if "request" parameter must be given. """
    def __init__(self, function, plugin):
        self.__func__ = function
        self.__plugin__ = plugin
        self.__exportable__ = True

    def __call__(self, request, *args, **kw):
        self.__exportable__ = True
        if hasattr(request, 'settings'):
            distant_url = request.settings.get('proxy-%s-distant_url' % self.__plugin__, None)
            if distant_url == None:
                return self.__func__(request, *args, **kw)
            else:
                imp = importer.Importer()
                imp['distant_url']  = distant_url
                imp['ssl_cert']     = request.settings.get('proxy-%s-ssl_cert' % self.__plugin__, None)
                imp['ssl_key']      = request.settings.get('proxy-%s-ssl_key' % self.__plugin__, None)
                return imp.call(self.__plugin__, self.__func__.__name__, *args, **kw)
        else:
            return self.__func__(request, *args, **kw)

""" DECORATORS """
def render(function=None, **kwds):
    """ This decorator MUST wrap any controller methods. """
    if function: return _CheckRenderMode(function, **kwds)
    def __nested__(func):
        return _CheckRenderMode(func, **kwds)
    return __nested__

def exportable(function):
    """ Define the function as "accessible by the Importer".
    This decorator MUST be the FIRST decorator used. """
    return _Export(function)

def proxy_func(plugin):
    """ Define the function as "accessible by the Importer".
    This decorator MUST be the FIRST decorator used. """
    def __nested__(func):
        return _Proxy(func, plugin)
    return __nested__
