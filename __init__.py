from django.http import HttpResponse

def index(request):
    """ Default index page. """
    return HttpResponse("<h1>It works!</h1>")
