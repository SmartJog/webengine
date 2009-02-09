# Create your views here.

from django.http import HttpResponse
import django.shortcuts
from webengine.utils import *

@render(view='fanfan')
def index(request):
    return (500, {'msg': 'pierrot'})
