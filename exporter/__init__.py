import simplejson as json
from webengine.importer import Importer, ImporterError
from webengine.utils.decorators import render
from webengine.utils.log import logger

@render(output='pickle')
def dispatch(request, *args, **kw):
    """
        Called when a URL created by exporter.urls.create_patterns() match.
        Perform somes checks, call the importer, and returns.
        Method name can be passed as:
        /module/method/ or /module/module/module/method/
        Arguments of the method MUST be passed as pickle in POST data.

        This method is not meant to be called directly with a web browser.

        The Importer() instance is stored in session.
    """

    base = kw.pop('base')
    modules = kw.pop('modules')

    # Create Importer() if not already present in session.
    if '__importer__' not in request.session:
        request.session['__importer__'] = Importer()
        # Bound to EXPORT_MODULES from configuration
        from webengine.exporter import settings
        request.session['__importer__'].bound(settings.EXPORT_MODULES)

    full_path = base + '.' + modules.replace('/', '.')
    mod, met = full_path.rsplit('.', 1)

    # GET request ?
    # Only method call without args or attributes. (from a webbrowser)
    if request.method == 'GET':
        try:
            return (200, request.session['__importer__'].get(mod, met))
        except ImporterError, e:
            logger.debug("Exporter: Catched   : " + e.msg)
            logger.debug("Exporter: Traceback : " + e.traceback)
            return (500, {'msg': e.msg, 'traceback': e.traceback})
    # POST ?
    # Method call with args, instantiations
    elif request.method == 'POST':
        try:
            import cPickle
            # Do not save in session during call() call.
            request.session.modified = False

            data = cPickle.loads(request.raw_post_data)
            # Cause args is a tuple, create a list before.
            args = list(args)
            if data.get('args'): args += data['args']
            kw.update(data['kw'])

            ret = None
            t = data['type']
            if t == 'call': ret = request.session['__importer__'].call(mod, met, *args, **kw)
            elif t == 'get': ret = request.session['__importer__'].get(mod, met)
            elif t == 'set': ret = request.session['__importer__'].set(mod, met, kw.pop('value'))
            elif t == 'instantiate': ret = request.session['__importer__'].instantiate(kw.pop('variable'), mod, met, *args, **kw)
            # Force session to be saved (should be pickable now).
            request.session.modified = True
            return (200, ret)
        except ImporterError, e:
            logger.debug("Exporter: Catched   : " + e.msg)
            logger.debug("Exporter: Traceback : " + e.traceback)
            return (500, {'msg': e.msg, 'traceback': e.traceback})
