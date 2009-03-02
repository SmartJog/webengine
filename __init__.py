from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

def index(request):
    """ Default index page. """
    if settings.DEFAULT_URL != '':
        return HttpResponseRedirect(settings.DEFAULT_URL)
    return HttpResponse("<h1>It works!</h1>")
