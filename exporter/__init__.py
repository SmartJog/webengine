import simplejson as json
from importer import Importer, ImporterError
from webengine.utils.decorators import render
from webengine.utils.log import logger

@render(output='pickle')
def dispatch(request, *args, **kw):
    """
        Perform somes checks, call the importer, and returns.
        Arguments of the method MUST be passed as pickle in POST data.
        This method is not meant to be called directly with a web browser.
        The Importer() instance is stored in session.
    """

    base = kw.pop('base')
    modules = kw.pop('modules')

    # Create Importer() if not already present in session.
    if '__importer__' not in request.session:
        request.session['__importer__'] = Importer()

    full_path = base.replace('/', '.') + '.' + modules.replace('/', '.')
    mod, met = full_path.rsplit('.', 1)
    module = __import__(mod, {}, {}, [''])
    callee = getattr(module, met)
    if not hasattr(callee, '__exportable__'):
        logger.debug("Exporter: method not exportable: " + full_path)
        return (200, Exception("Method not exportable"))

    # GET request ?
    # Only method call without args or attributes. (from a webbrowser)
    if request.method == 'GET':
        try:
            return (200, request.session['__importer__'].get(mod, met))
        except ImporterError, e:
            logger.debug("Exporter: Catched: " + e.traceback)
            return (500, {'msg': e.msg, 'traceback': e.traceback})
    # POST ?
    # Method call with args, instantiations
    elif request.method == 'POST':
        try:
            import cPickle

            data = cPickle.loads(request.raw_post_data)
            # Cause args is a tuple, create a list before.
            args = list(args)
            if data.get('args'): args += data['args']
            kw.update(data['kw'])
            kw.update({'__request__': request})

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
            logger.debug("Exporter: ImporterError catched: " + str(e))
            return (500, {'msg': e.msg, 'traceback': e.traceback})
        except Exception, e:
            import traceback
            logger.debug("Exporter: Catched: " + str(e))
            return (500, {'msg': str(e), 'traceback': traceback.format_exc()})
