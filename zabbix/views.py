# -*- coding: utf-8 -*-

from django.shortcuts import render
from nettools.forms import DeviceForm
from django.core.mail import send_mail
from .zabbix_api_methods import zabbix_add_host
from secrets.secrets import ZABBIX_EMAIL_DESTINATIONS


def add_host(request):
    added = False
    zabbix_error = False
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            r = zabbix_add_host(cd['hostname'], cd['ip_address'], cd['group_name'], cd['template_name'], cd['snmp_community'], cd['status'])
            if r is True:
                added = True
                message = 'New host ' + str(cd['ip_address']) + ' ' + str(cd['hostname'])
                send_mail('New host', message, 'zabbix@bashkirenergo.ru', ZABBIX_EMAIL_DESTINATIONS)
            else:
                zabbix_error = r
    else:
        form = DeviceForm()
    return render(request, 'add_host.html', {'form': form, 'added': added, 'zabbix_error': zabbix_error})
