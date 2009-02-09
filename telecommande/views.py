from webengine.utils import render

@render(view='index')
def index(request):
    return {}
