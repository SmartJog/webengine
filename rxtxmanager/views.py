from webengine.utils import *

@render(view='index', output='html')
def index(request):
    toto = [1, 2, 3]
    return {'toto': toto}
