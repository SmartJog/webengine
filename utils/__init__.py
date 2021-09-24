import os
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _


def get_valid_plugins():
    """
    Returns a list of valid webengine plugins.
    Returns:    [('name', <module 'webengine.name'>), ...]
    """
    try:
        webengine = __import__("webengine")
    except ImportError:
        return []

    def __isplugin(mod_name):
        """Nested method of get_valid_plugins, tries to import webengine.<mod_name>.urls."""
        mod = None
        try:
            mod = __import__("webengine." + mod_name, {}, {}, [""])
        except Exception, _error:
            return []
        try:
            __import__("webengine." + mod_name + ".urls", {}, {}, [""])
        except Exception:
            return []
        return mod_name, mod

    wdir = webengine.__path__[0]
    # Map os.listdir(wdir) to isplugin, and then "filter" elements that are None
    return [
        dir
        for dir in map(
            __isplugin,
            [d for d in os.listdir(wdir) if os.path.isdir(os.path.join(wdir, d))],
        )
        if dir
    ]


def webengine_template_processor(request):
    """
    This method is called by the RequestContext() object.
    It adds to the template variables the profile, etc..
    Each key in the returned dict will be available as is
    when processing the template.
    Add everything you need in every template.
    """
    log = logging.getLogger("webengine.utils.webengine_template_processor")
    log.setLevel(logging.DEBUG)

    from django.conf import settings

    modules = get_valid_plugins()
    menus = []

    auth_mods = settings.AUTHORIZED_MODS or [m[0] for m in modules]
    for mod in modules:
        try:
            if hasattr(mod[1].urls, "menus"):
                menus.extend(mod[1].urls.menus)
        except AttributeError:
            continue

    return {
        "profile": settings.PROFILE,
        "menus": menus,
        "WEBENGINE_SKIN": getattr(settings, "SKIN", "front/base.html"),
    }


def default_view(request):
    """Default index page."""
    try:
        if request.settings.get("default_url", None):
            return HttpResponseRedirect(reverse(request.settings["default_url"]))
        if settings.DEFAULT_URL != "":
            return HttpResponseRedirect(reverse(settings.DEFAULT_URL))
    except NoReverseMatch, _error:
        return HttpResponse("<h1>It works!</h1>")
