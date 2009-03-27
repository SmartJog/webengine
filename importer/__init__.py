"""
    Intented to be use like this:

    importer.(<module>.)+<function>(args)
"""

#import simplejson as json
#from webengine.utils.log import logger
#import traceback
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
        return getattr(self.__objinst__, method)(*args, **kw)

class ImporterModule(ImporterBase):
    def __init__(self, conf, module):
        """ Takes configuration from Importer() instance. """
        super(ImporterBase, self).__init__(conf)
        self.__mod__ = module
        try:
            self.__objinst__ = __import__(self.__mod__, {}, {}, [''])
        except ImportError, e:
            raise ImporterError(str(e))

class ImporterVariable(ImporterBase):
    def __init__(self, conf, module, klass, *args, **kw):
        super(ImporterBase, self).__init__(conf)
        self.__mod__ = module
        self.__klass__ = klass
        try:
            #Instanciate the object
            self.__objinst__ = getattr(__import__(self.__mod__, {}, {}, ['']), klass)(*args, **kw)
        except ImportError, e:
            raise ImporterError(str(e))

class Importer(ImporterBase):
    """ Main class. Contains all modules. """
    def __init__(self):
        super(Importer, self).__init__()
        self.__scope__ = {}
        self.__bound__ = None

    def call(self, module, method, *args, **kw):
        """
            Perform a call to module.method, passing the given *args, **kw.
            Return: module.method return.
        """
        # Module already in scope?
        if module not in self.__scope__.keys():
            first = module.split('.')[0]
            # Module out of bounds?
            if self.__bound__ and first not in self.__bound__:
                raise ImporterError('Module %s out of bounds' % first)
            # Add module to scope and import
            self.__scope__[module] = ImporterModule(self.__conf__, module)
        # Call ImporterModule.call() that does the real job
        return self.__scope__[module].call(method, *args, **kw)

    def get(self, module, attr):
        """ Retrieve an attr from the given module. """
        pass

    def set(self, module, attr, value):
        """ Used to set module.attr to value. """
        pass

    def instantiate(self, variable, module, klass, *args, **kw):
        """
            Add in the current scope a 'klass' instance from module.
            Similar to module.klass(*args, **kw).
            variable will be usable in the scope as others modules.
        """
        if variable in self.__scope__.keys(): return
        self.__scope__[variable] = ImporterVariable(self.__conf__, module, klass, *args, **kw)

    def bound(self, bound):
        """ Bound Importer scope to "bound" list. """
        self.__bound__ = bound

if __name__ == '__main__':
    imp = Importer()
    imp['distant_uri'] = 'https://sj-dev-1.lab/'
    print imp.call('os.path', 'basename', '/sdf/xcv/wer/sdf/swww')
    imp.instantiate('err', 'os', 'error')
    print imp.call('err', 'listdir', '/path/to/lol')
