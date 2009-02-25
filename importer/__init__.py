"""
    Intented to be use like this:

    importer.(<module>.)+<function>(args)
"""

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

    def __getattr__(self, key):
        if not (key in self.__dict__):
            self.__dict__[key] = Module(self.__importer__, self, key)
        return self.__dict__[key]

    def __call__(self, *args, **kw):
        """ This Module instance will act like a method. """
        # Resolve
        #FIXME: Will be distant or local, only local by now.
        # Construct module path.
        curr = self
        path = []
        while curr.__parent__ is not None:
            path.append(curr.__name__)
            curr = curr.__parent__
        path.append(curr.__name__)
        path.reverse()
        path = '.'.join(path)
        module, method = path.rsplit('.', 1)
        # Let exception be raised? Raise a custom one ?
        m = __import__(module, {}, {}, [''])
        f = getattr(m, method)
        ret = f(*args, **kw)
        return ret

    def __repr__(self):
        """ Represent instance as a string. """
        return "<%s parent=%s importer=%s>" % (self.__class__.__name__, self.__parent__, self.__importer__)
    __str__ = __repr__

class Importer(object):
    """ Main class. Contains all modules. """
    def __init__(self):
        self.__modules__ = {}
        self.__request__ = None

    def __getattr__(self, key):
        """ importer.key -> Returns a Module() instance. """
        if not (key in self.__modules__):
            raise KeyError("Module %s does not exist" % key)
        return self.__modules__[key]

    def setRequest(self, req):
        """
            Set the "context" by giving the current request.
            Importer() will decide (based on the request), if data
            will be fetch locally or remotely.
        """
        self.__request__ = req
        # Do what we need to do to decide where to get the data
        # based on request.user, or other things.

importer = Importer()
