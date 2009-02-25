import os

def get_valid_plugins():
    """
        Returns a list of valid webengine plugins.
        Returns:    [('name', <module 'webengine.name'>), ...]
    """
    def __isplugin(dir):
        """ Nested method of get_valid_plugins, tries to import webengine.<dir>.urls. """
        # Try to import webengine.<dir>.urls
        mod = None
        try:
            __import__('webengine.' + dir + '.urls', {}, {}, [''])
            mod = getattr(__import__('webengine'), dir)
        except ImportError:
            return None
        return dir, mod

    wdir = os.getcwd()
    # Map os.listdir(wdir) to isplugin, and then "filter" elements that are None
    dirs = [dir for dir in map(__isplugin, [d for d in os.listdir(wdir) if os.path.isdir(os.path.join(wdir, d))]) if dir]
    return dirs
