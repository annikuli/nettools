from django.shortcuts import render
from nettools.forms import VsiForm
from .models import Vsi
from devices.models import Device
import xlwt
from django.http import HttpResponse


def display_all_vsi(request):
    added = False
    edit = False
    edit_id = False
    err = False
    if request.method == 'POST':
        print('Info: Request method POST')
        vsis = VsiForm(request.POST, prefix='vsi_form')
        if vsis.is_valid():
            print('Info: VSI Form is valid')
            print(vsis)  ## TODO: make manual check if at least 2 switches are chosen
            try:
                vsis.save()
                added = True
            except Exception as e:
                print('Error: VSI data has not been saved in VSI DB.')
                added = False
        else:
            print('Error: VSI Form is not valid')
            print(vsis.errors)
            err = vsis
    else:
        print('Info: Request method GET')
        if 'edit' in request.GET:
            edit_id = request.GET['edit']
            print('Info: Trying to edit "{}" from VSI DB.'.format(edit_id))
            try:
                instance = Vsi.objects.get(id=edit_id)
            except Exception as e:
                print('Error: "{}" can not be edited.'.format(edit))
                print('Error: {}'.format(e))
        if 'new' in request.GET:
            new_id = request.GET['new']
            instance = Vsi.objects.get(id=new_id)
            vsis = VsiForm(request.GET, prefix='update', instance=instance)
            if vsis.is_valid():
                print('Info: VSI Form is valid')
                try:
                    vsis.save()
                    print('Info: VSI {} updated'.format(instance))
                except Exception as e:
                    print('Error: VSI data has not been saved in VSI DB.')
            else:
                print('Error: VSI Form is not valid')
                print(vsis.errors)
                err = vsis
        if 'del' in request.GET:
            d = request.GET['del']
            print('Info: Trying to delete "{}" from VSI DB.'.format(d))
            try:
                Vsi.objects.filter(id=d).delete()
                print('Info: "{}" has been deleted from VSI DB.'.format(d))
            except Exception as e:
                print('Error: "{}" can not be removed from VSI DB.'.format(d))
                print('Error: {}'.format(e))
        if 'q' in request.GET:
            search = request.GET['q']
            if search != '':
                print('Info: Searching for "{}" in VSI DB.'.format(search))
                vsis = Vsi.objects.all().prefetch_related('switch').filter(switch__hostname__icontains=search)
                # vsis = Vsi.objects.filter(switch__icontains=search)
                return render(request, 'vsi.html', {'vsis': vsis})
    vsis = Vsi.objects.all().order_by('name')
    v = []
    for vsi in vsis:
        v.append(vsi.vsi_id)
    first_allowed_vsi_id = find_allowed_vsi_id(v)
    devices = Device.objects.all().order_by('hostname')
    vsi_form = VsiForm(prefix='vsi_form')
    print('Info: Default output.')
    print(edit_id)
    return render(request, 'vsi.html', {'vsis':vsis,
                                        'added':added,
                                        'err':err,
                                        'edit':edit,
                                        'edit_id':edit_id,
                                        'devices': devices,
                                        'vsi_form': vsi_form,
                                        'first_allowed_vsi_id': first_allowed_vsi_id})


def find_allowed_vsi_id(vsi_ids):
    for i in range(1,len(vsi_ids)+1):
        if i != sorted(vsi_ids)[i-1]:
            return i
    return len(vsi_ids)+1


def export_vsi_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vsis.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Devices')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['addition_date', 'name', 'vsi_id', 'description', 'switch',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_style = xlwt.XFStyle()
    date_style.num_format_str = 'dd/mm/yyyy'

    rows = Vsi.objects.all().values_list('addition_date', 'name', 'vsi_id', 'description', 'switch__hostname')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 0:
                ws.write(row_num, col_num, row[col_num], date_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


