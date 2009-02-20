from webengine.utils.decorators import render

@render(view='index')
def index(request):
    return {}
