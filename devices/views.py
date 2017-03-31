from django.shortcuts import render
from nettools.forms import AccessSwitchForm, AccessSwitchConfigForm, ZabbixForm
from .models import AccessSwitch, AccessSwitchConfig
from django.db import IntegrityError
from .generator import generator
from zabbix.zabbix_api_methods import zabbix_add_host


def generate_config(request):
    added = False
    device_error = False
    zabbix_error = False
    generated_config = ''
    if request.method == 'POST':
        print('Info: Request method POST')
        device = AccessSwitchForm(request.POST, prefix='device')
        config = AccessSwitchConfigForm(request.POST, prefix='config')
        zab = ZabbixForm(request.POST, prefix='zabbix')

        if device.is_valid() and config.is_valid() and zab.is_valid():
            print('Info: DEVICE AND CONFIG Forms are valid')
            cd = device.cleaned_data
            cd2 = config.cleaned_data
            cd3 = zab.cleaned_data
            device_data = AccessSwitch(
                hostname=cd['hostname'],
                addition_date=cd['addition_date'],
                model=cd['model'],
                ports=cd['ports'],
                po=cd['po'],
                purchase=cd['purchase'],
                description=cd['description']
                )
            if not AccessSwitchConfig.objects.filter(ip=cd2['ip']):
                print('Info: No duplicate IPs in AccessSwitchConfig DB')
                try:
                    device_data.save()
                    print('Info: DEVICE data saved in AccessSwitch DB.')
                    config_data = AccessSwitchConfig(
                        hostname=device_data,
                        mgmt_vlan=cd2['mgmt_vlan'],
                        ip=cd2['ip'],
                        mask=cd2['mask'],
                        gw=cd2['gw'],
                        snmp_location=cd2['snmp_location']
                    )
                    config_data.save()
                    print('Info: CONFIG data saved in AccessSwitchConfig DB.')
                    generated_config = generator(
                        model=cd['model'],
                        hostname=cd['hostname'],
                        ports=cd['ports'],
                        mgmt_vlan=cd2['mgmt_vlan'],
                        ip=cd2['ip'],
                        mask=cd2['mask'],
                        gw=cd2['gw'],
                        snmp_location=cd2['snmp_location']
                    )
                    r = zabbix_add_host(cd['hostname'], cd2['ip'], cd3['group_name'], cd3['template_name'],
                                        cd2['snmp_community'], cd3['status'])
                    if r is True:
                        added = True
                    else:
                        zabbix_error = r
                except IntegrityError as e:
                    print('Error: {}'.format(e))
                    device_error = e
            else:
                device_error = 'Host with this IP already exists'
        else:
            print(device.errors)
            print(config.errors)
    else:
        print('Info: Request method GET')
        device = AccessSwitchForm(prefix='device')
        config = AccessSwitchConfigForm(prefix='config')
        zab = ZabbixForm(prefix='zabbix')
    return render(request, 'generate_config.html',
                  {'device': device,
                   'config': config,
                   'zabbix': zab,
                   'device_error': device_error,
                   'generated_config':generated_config,
                   'added': added,
                   'zabbix_error': zabbix_error}
                  )


def display_db(request):
    if 'o' in request.GET:
        o = request.GET['o']
        devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by(o)
        # devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by('hostname__purchase')
    else:
        devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by('hostname')
    return render(request, 'list.html', {'devices': devices})
