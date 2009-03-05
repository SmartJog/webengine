"""
    Intented to be use like this:

    importer.(<module>.)+<function>(args)
"""

import simplejson as json

class ImporterError(Exception):
    """ Raised when something happen in Importer."""
    def __init__(self, msg):
        self.__msg__ = msg

    def __repr__(self):
        return self.__msg__
    __str__ = __repr__

# Transparent to module ?
# Recuperation du module sur /module/get_module, creation de l'objet a partir du retour.
class Module(object):
    """
        Represent a local/distant python module.
        When __getattr__ is called, spawn a new instance of Module() and add
        it to the __dict__.
        Module instance can also be called like a method, in this case, it
        will act like a method. This has been made to allow syntax like
        module1.module2.module3...method()
    """
    def __init__(self, imp, parent, name):
        self.__name__ = name
        self.__parent__ = parent
        self.__importer__ = imp
        self.__islocal__ = True

    def __getattr__(self, key):
        if not (key in self.__dict__):
            self.__dict__[key] = Module(self.__importer__, self, key)
        return self.__dict__[key]

    def __call__(self, *args, **kw):
        """
            This Module instance will act like a method.
            If method is POST, args are in the raw_post_data,
            serialized in JSON.
            POST datas must be formatted like:
            {'args': ['arg1', 'arg2', 'arg3',..],
             'kw': {
                'kw1': 42,
                'kw2': 'kw2',
                ...
             }
            }
        """
        # Construct module path.
        curr = self
        path = []
        while curr.__parent__ is not None:
            path.append(curr.__name__)
            curr = curr.__parent__
        path.append(curr.__name__)
        path.reverse()
        if self.__islocal__:
            return self.__local_call__(path, *args, **kw)
        else:
            path = '/'.join(path) + '/'
            return self.__distant_call__(path, *args, **kw)

    def __repr__(self):
        """ Represent instance as a string. """
        return "<%s parent=%s importer=%s>" % (self.__class__.__name__, self.__parent__, self.__importer__)
    __str__ = __repr__

    def __local_call__(self, path, *args, **kw):
        """ We perform a local call, directly import and call the method. Return as is. """
        req = importer.__request__
        if req and req.method == 'POST':
            #Merge POST data with kw
            data = json.JSONDecoder().decode(req.raw_post_data)
            #FIXME: json.loads returns unicode strings...
            d = dict([(str(k), str(v)) for k,v in data['kw'].items()])
            kw.update(d)
            # Cause args is a tuple, create a list before.
            args = list(args)
            args += data['args']

        module, method = '.'.join(path[:-1]), path[-1]
        m = __import__(module, {}, {}, [''])
        f = getattr(m, method)
        # If f is callable, it's a function, otherwise, a module attribute.
        if callable(f): ret = f(*args, **kw)
        else: ret = f
        return ret

    def __distant_call__(self, path, *args, **kw):
        """ Method which performs a distant call to another exporter. """
        import urllib2
        # Perform the distant call.
        data = json.JSONEncoder().encode({'args': args, 'kw': kw})
        try:
            req = urllib2.Request(url='https://sj-dev-1.lab/' + path, data=data)
            f = urllib2.urlopen(req)
            #TODO: Call the right deserializer.
            datas = f.read()
            if datas == '': return None # Nothing to return
            ret = json.JSONDecoder().decode(datas)
            return ret
        except urllib2.HTTPError, e:
            raise ImporterError("Method %s missing or not allowed." % path)

class Importer(object):
    """ Main class. Contains all modules. """
    def __init__(self):
        self.__modules__ = {}
        self.__request__ = None

    def __getattr__(self, key):
        """
            importer.key -> Returns a Module() instance.
            This module is not linked with EXPORT_MODULES from exporter plugin.
            There's no check if plugin exists (checked on __call__) or is in
            EXPORT_MODULES tuple.
        """
        if not (key in self.__modules__):
            self.__modules__[key] = Module(self, None, key)
        return self.__modules__[key]

    def set_request(self, req):
        """
            Set the "context" by giving the current request.
            Importer() will decide (based on the request), if data
            will be fetch locally or remotely.
        """
        self.__request__ = req
        # Do what we need to do to decide where to get the data
        # based on request.user, or other things.

importer = Importer()
