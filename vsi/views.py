from django.shortcuts import render
from nettools.forms import VsiForm
from .models import Vsi
# Create your views here.


def display_all_vsi(request):
    vsis = Vsi.objects.all()
    print('Info: Default output.')
    return render(request, 'vsi.html', {'vsis':vsis})
