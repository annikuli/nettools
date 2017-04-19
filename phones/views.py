from django.shortcuts import render
from .models import Contact
# Create your views here.

def display_phone_book(request):
    if 'q' in request.GET:
        search = request.GET['q']
        if search != '':
            print('Info: Searching for "{}" in Contact DB.'.format(search))
            contacts = Contact.objects.filter(organization__icontains=search)
            return render(request, 'phones.html', {'contacts': contacts})
    contacts = Contact.objects.all().order_by('organization')
    print('Info: Default output.')
    return render(request, 'phones.html', {'contacts':contacts})