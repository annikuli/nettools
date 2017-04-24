from django.shortcuts import render
from .models import Contact
from nettools.forms import ContactForm
import xlwt
from django.http import HttpResponse


def display_phone_book(request):
    added = False
    edit = False
    edit_id = False
    err = False
    if request.method == 'POST':
        print('Info: Request method POST')
        contacts = ContactForm(request.POST, prefix='contact')
        if contacts.is_valid():
            print('Info: Contact Form is valid')
            try:
                contacts.save()
                added = True
            except Exception as e:
                print('Error: Contact data has not been saved in Contact DB.')
                added = False
        else:
            print('Error: Contact Form is not valid')
            print(contacts.errors)
            err = contacts
    else:
        print('Info: Request method GET')
        if 'edit' in request.GET:
            edit_id = request.GET['edit']
            print('Info: Trying to edit "{}" from Contact DB.'.format(edit_id))
            try:
                instance = Contact.objects.get(id=edit_id)
            except Exception as e:
                print('Error: "{}" can not be edited.'.format(edit))
                print('Error: {}'.format(e))
        if 'new' in request.GET:
            new_id = request.GET['new']
            instance = Contact.objects.get(id=new_id)
            contacts = ContactForm(request.GET, prefix='update', instance=instance)
            if contacts.is_valid():
                print('Info: Contact Form is valid')
                try:
                    contacts.save()
                    print('Info: Contact {} updated'.format(instance))
                except Exception as e:
                    print('Error: Contact data has not been saved in Contact DB.')
            else:
                print('Error: Contact Form is not valid')
                print(contacts.errors)
                err = contacts
        if 'del' in request.GET:
            d = request.GET['del']
            print('Info: Trying to delete "{}" from Contact DB.'.format(d))
            try:
                Contact.objects.filter(id=d).delete()
                print('Info: "{}" has been deleted from Contact DB.'.format(d))
            except Exception as e:
                print('Error: "{}" can not be removed from Contact DB.'.format(d))
                print('Error: {}'.format(e))
        if 'q' in request.GET:
            search = request.GET['q']
            if search != '':
                print('Info: Searching for "{}" in Contact DB.'.format(search))
                contacts = Contact.objects.filter(organization__icontains=search)
                return render(request, 'phones.html', {'contacts': contacts})
    contacts = Contact.objects.all().order_by('organization')
    print('Info: Default output.')
    print(edit_id)
    return render(request, 'phones.html', {'contacts':contacts, 'added':added, 'err':err, 'edit':edit, 'edit_id':edit_id})


def export_phones_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="phones.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Phones')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Имя', 'Организация', 'Телефон', 'E-mail', 'Комментарий',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Contact.objects.all().values_list('name', 'organization', 'phone_number', 'email', 'description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response