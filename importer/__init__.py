"""
    Intented to be use like this:

    importer.(<module>.)+<function>(args)
"""

#import simplejson as json
#from webengine.utils.log import logger
import traceback
#
class ImporterError(Exception):
    """ Raised when something happen in Importer."""
    def __init__(self, msg, local=True, traceback=''):
        self.msg = msg
        self.local = local
        self.traceback = traceback

    def __repr__(self):
        return self.msg or 'Importer failed'
    __str__ = __repr__
#
## Transparent to module ?
## Recuperation du module sur /module/get_module, creation de l'objet a partir du retour.
#class Module(object):
#    """
#        Represent a local/distant python module.
#        When __getattr__ is called, spawn a new instance of Module() and add
#        it to the __dict__.
#        Module instance can also be called like a method, in this case, it
#        will act like a method. This has been made to allow syntax like
#        module1.module2.module3...method()
#    """
#    def __init__(self, imp, parent, name):
#        self.__name__ = name
#        self.__parent__ = parent
#        self.__importer__ = imp
#        self.__islocal__ = True
#
#    def __getattr__(self, key):
#        if not (key in self.__dict__):
#            self.__dict__[key] = Module(self.__importer__, self, key)
#        return self.__dict__[key]
#
#    def __call__(self, *args, **kw):
#        """
#            This Module instance will act like a method.
#            If method is POST, args are in the raw_post_data,
#            serialized in JSON.
#            POST datas must be formatted like:
#            {'args': ['arg1', 'arg2', 'arg3',..],
#             'kw': {
#                'kw1': 42,
#                'kw2': 'kw2',
#                ...
#             }
#            }
#        """
#        # Construct module path.
#        curr = self
#        path = []
#        while curr.__parent__ is not None:
#            path.append(curr.__name__)
#            curr = curr.__parent__
#        path.append(curr.__name__)
#        path.reverse()
#        if self.__islocal__:
#            return self.__local_call__(path, *args, **kw)
#        else:
#            path = '/'.join(path) + '/'
#            return self.__distant_call__(path, *args, **kw)
#
#    def __repr__(self):
#        """ Represent instance as a string. """
#        return "<%s parent=%s importer=%s>" % (self.__class__.__name__, self.__parent__, self.__importer__)
#    __str__ = __repr__
#
#    def __local_call__(self, path, *args, **kw):
#        """ We perform a local call, directly import and call the method. Return as is. """
#        req = importer.__request__
#        if req and req.method == 'POST':
#            #Merge POST data with kw
#            data = json.JSONDecoder().decode(req.raw_post_data)
#            #FIXME: json.loads returns unicode strings...
#            d = dict([(str(k), str(v)) for k,v in data['kw'].items()])
#            kw.update(d)
#            # Cause args is a tuple, create a list before.
#            args = list(args)
#            args += data['args']
#
#        module, method = '.'.join(path[:-1]), path[-1]
#        try:
#            m = __import__(module, {}, {}, [''])
#            f = getattr(m, method)
#            # If f is callable, it's a function, otherwise, a module attribute.
#            if callable(f): ret = f(*args, **kw)
#            else: ret = f
#            return ret
#        except Exception, e:
#            logger.debug('Importer: Raised: ' + '.'.join(path) + ' - ' + str(e))
#            raise ImporterError('.'.join(path) + ' - ' + str(e), local=True, traceback=traceback.format_exc()) # Re raise the exception as an ImporterError
#
#    def __distant_call__(self, path, *args, **kw):
#        """
#            Method which performs a distant call to another exporter.
#            It calls the distant 'exporter'.
#            Two possibilities:
#                - Success, 200 returned, datas returned as JSON. Nothing to do with this, just return after decode.
#                - Error, raise ImporterError.
#        """
#        import urllib2
#        # Perform the distant call.
#        try:
#            data = json.JSONEncoder().encode({'args': args, 'kw': kw})
#            req = urllib2.Request(url='https://sj-dev-1.lab/' + path, data=data)
#            f = urllib2.urlopen(req)
#            #TODO: Call the right deserializer.
#            datas = f.read()
#            if datas == '': return None # Nothing to return
#            data_decoded = json.JSONDecoder().decode(datas)
#            return data_decoded
#        except urllib2.HTTPError, e:
#            if e.code == 404:
#                raise ImporterError("Method %s missing." % path, local=False, traceback=traceback.format_exc())
#            elif e.code == 500:
#                data_decoded = json.JSONDecoder().decode(e.read()) # Read exception
#                raise ImporterError(data_decoded['msg'], local=False, traceback=data_decoded['traceback'])

# New importer BEGINGS HERE

class ImporterBase(object):
    """
        Base class for both ImporterModule and ImporterVariable.
        Provide call/get/set methods, relying on proper self.__objinst__ object.
        ImporterModule and ImporterVariable are in charge of creating the appropriate object.
    """
    def __init__(self, conf={}):
        self.__conf__ = conf
        self.__objinst__ = None

    def __getitem__(self, key):
        """
            Used to retrieve data from Importer configuration.
            Let exceptions be thrown.
        """
        return self.__conf__[key]

    def __setitem__(self, key, value):
        """ Set configuration key. """
        self.__conf__[key] = value

    def __delitem__(self, key):
        """ Delete configuration key. """
        del self.__conf__[key]

    def call(self, method, *args, **kw):
        """ Getattr self.__objinst__ which will be a module instance or a variable instance. """
        try:
            return getattr(self.__objinst__, method)(*args, **kw)
        except Exception, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

    def get(self, attr):
        """ Getattr self.__objinst__ and returns. """
        try:
            return getattr(self.__objinst__, attr)
        except AttributeError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

    def set(self, attr, value):
        """ Set value for self.__objinst__.attr. """
        try:
            setattr(self.__objinst__, attr, value)
        except AttributeError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

class ImporterModule(ImporterBase):
    def __init__(self, conf, module):
        """ Takes configuration from Importer() instance. """
        super(ImporterBase, self).__init__(conf)
        self.__mod__ = module
        try:
            # Just try to import it
            __import__(self.__mod__, {}, {}, [''])
        except ImportError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

    def call(self, method, *args, **kw):
        """
            Override ImporterBase.call, but call it after.
            We need to do this, because if we store the module instance in __objinst__,
            when saving the session, module is tried to be pickled, and it fails.
        """
        try:
            self.__objinst__ = __import__(self.__mod__, {}, {}, [''])
        except ImportError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())
        ret = ImporterBase.call(self, method, *args, **kw)
        # We need to remove from the object, cause a lot of module are not "pickable"
        self.__objinst__ = None
        return ret

class ImporterVariable(ImporterBase):
    def __init__(self, conf, module, klass, *args, **kw):
        super(ImporterBase, self).__init__(conf)
        self.__mod__ = module
        self.__klass__ = klass
        try:
            #Instantiate the object
            self.__objinst__ = getattr(__import__(self.__mod__, {}, {}, ['']), klass)(*args, **kw)
        except Exception, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

class Importer(ImporterBase):
    """
        Main class. Contains all modules.
        Call/get/set/instantiate always check if execution must be done remotely.
    """
    def __init__(self):
        super(Importer, self).__init__()
        self.__scope__ = {}
        self.__bound__ = None

    def call(self, module, method, *args, **kw):
        """
            Perform a call to module.method, passing the given *args, **kw.
            Override ImporterBase.call()
            Return: module.method return.
        """
        if 'distant_url' in self.__conf__.keys():
            mod = '.'.join((module, method))
            return self.__perform_distant__(mod, 'call', *args, **kw)
        self.__load_module__(module)
        return self.__scope__[module].call(method, *args, **kw)

    def get(self, module, attr):
        """ Retrieve an attr from the given module. """
        if 'distant_url' in self.__conf__.keys():
            mod = '.'.join((module, attr))
            return self.__perform_distant__(mod, 'get')
        self.__load_module__(module)
        return self.__scope__[module].get(attr)

    def set(self, module, attr, value):
        """ Used to set module.attr to value. """
        if 'distant_url' in self.__conf__.keys():
            mod = '.'.join((module, attr))
            return self.__perform_distant__(mod, 'set', value=value)
        self.__load_module__(module)
        return self.__scope__[module].set(attr, value)

    def instantiate(self, variable, module, klass, *args, **kw):
        """
            Add in the current scope a 'klass' instance from module.
            Similar to module.klass(*args, **kw).
            variable will be usable in the scope as others modules.
        """
        if 'distant_url' in self.__conf__.keys():
            mod = '.'.join((module, klass))
            return self.__perform_distant__(mod, 'instantiate', variable=variable, *args, **kw)
        if variable in self.__scope__.keys(): return
        self.__scope__[variable] = ImporterVariable(self.__conf__, module, klass, *args, **kw)

    def bound(self, bound):
        """ Bound Importer scope to "bound" list. """
        self.__bound__ = bound

    def __load_module__(self, module):
        """ Lookup for 'module' in scope, and if not present, create a ImporterModule object. """
        # Module already in scope?
        if module not in self.__scope__.keys():
            first = module.split('.')[0]
            # Module out of bounds?
            if self.__bound__ and first not in self.__bound__:
                raise ImporterError('Module %s out of bounds' % first)
            # Add module to scope and import
            self.__scope__[module] = ImporterModule(self.__conf__, module)

    def __perform_distant__(self, module, type, *args, **kw):
        """ Perform the distant call. """
        import urllib2, cPickle
        try:
            print module, type, args, kw
            path = module.replace('.', '/') + '/' #Force trailing slash
            # Should be able to select encoder
            # TODO: Create a wrapper for cPickle, pickle in fallback
            data = cPickle.dumps({'type': type, 'args': args, 'kw': kw}, cPickle.HIGHEST_PROTOCOL)
            req = urllib2.Request(url=self.__conf__['distant_url'] + path, data=data)
            f = urllib2.urlopen(req)
            data_read = f.read()
            if data_read == '': return None
            data_decoded = cPickle.loads(data_read)
            return data_decoded
        except urllib2.HTTPError, e:
            if e.code == 404:
                raise ImporterError("Method %s missing." % path, local=False, traceback=traceback.format_exc())
            elif e.code == 500:
                data_decoded = cPickle.loads(e.read()) # Read exception
                raise ImporterError(data_decoded['msg'], local=False, traceback=data_decoded['traceback'])
        except urllib2.URLError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())
        except cPickle.PickleError, e:
            raise ImporterError(str(e), traceback=traceback.format_exc())

if __name__ == '__main__':
    import os
    imp = Importer()
    print imp.call('os.path', 'join', 'LOL', 'mdr')
    imp['distant_url'] = 'https://sj-dev-3.lab/exporter/'
    imp.instantiate('ctx', 'sjio', 'Ctx')
    imp.instantiate('file', 'ctx', 'open', '/mnt/space/sjfs/repo/test_importer', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    imp.call('file', 'write', 'IMPORTER IS WORKING.DAMN!')
    imp.call('file', 'close')
