import os

def get_valid_plugins():
    """
        Returns a list of valid webengine plugins.
        Returns:    [('name', <module 'webengine.name'>), ...]
    """
    webengine = __import__('webengine')
    def __isplugin(mod_name):
        """ Nested method of get_valid_plugins, tries to import webengine.<mod_name>.urls. """
        mod = None
        try:
            __import__('webengine.' + mod_name + '.urls', {}, {}, [''])
            mod = getattr(webengine, mod_name)
        except ImportError:
            return None
        return mod_name, mod

    wdir = webengine.__path__[0]
    # Map os.listdir(wdir) to isplugin, and then "filter" elements that are None
    dirs = [dir for dir in map(__isplugin, [d for d in os.listdir(wdir) if os.path.isdir(os.path.join(wdir, d))]) if dir]
    return dirs
