from django.shortcuts import render
from .zabbix_api_methods import zabbix_add_host
from nettools.forms import DeviceForm

def add_host(request):
    added = False
    zabbix_error = False
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            r = zabbix_add_host(cd['hostname'], cd['ip_address'], cd['group_name'], cd['template_name'], cd['snmp_community'])
            if r is True:
                added = True
            else:
                zabbix_error = r
    else:
        form = DeviceForm()
    return render(request, 'add_host.html', {'form': form, 'added': added, 'zabbix_error': zabbix_error})
