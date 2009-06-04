import os
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


def get_valid_plugins():
    """
        Returns a list of valid webengine plugins.
        Returns:    [('name', <module 'webengine.name'>), ...]
    """
    try:
        webengine = __import__('webengine')
    except ImportError:
        return []
    def __isplugin(mod_name):
        """ Nested method of get_valid_plugins, tries to import webengine.<mod_name>.urls. """
        mod = None
        try:
            mod = __import__('webengine.' + mod_name, {}, {}, [''])
        except Exception, e:
            return []
        try:
            __import__('webengine.' + mod_name + '.urls', {}, {}, [''])
        except Exception:
            return []
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
            if request.user.has_perm('mods.' + mod[0]): menus.append(mod[1].urls.menus)
        except AttributeError:
            continue

    #Sort menus by position and alphabetical order
    def cmp_menu(x,y):
        if 'position' not in x or 'position' not in y:
            return 1
        if x['position'] > y['position']:
            return 1
        elif x['position'] == y['position']:
            return x['title'] > y['title']
        else:
            return -1
    menus.sort(cmp_menu)

    return {
        'profile': settings.PROFILE,
        'menus': menus,
    }

def default_view(request):
    """ Default index page. """
    if settings.DEFAULT_URL != '':
        return HttpResponseRedirect(settings.DEFAULT_URL)
    return HttpResponse("<h1>It works!</h1>")
