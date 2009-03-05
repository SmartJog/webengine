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
    return [dir for dir in map(__isplugin, [d for d in os.listdir(wdir) if os.path.isdir(os.path.join(wdir, d))]) if dir]

def webengine_template_processor(request):
    """
        This method is called by the RequestContext() object.
        It adds to the template variables the profile, etc..
        Each key in the returned dict will be available as is
        when processing the template.
        Add everything you need in every template.
    """
    from django.conf import settings
    modules = get_valid_plugins()
    menus = []
    for mod in modules:
        try:
            m = mod[1].urls.menus
            menus.append(m)
        except AttributeError:
            continue
    return {
        'profile': settings.PROFILE,
        'menus': menus,
    }
