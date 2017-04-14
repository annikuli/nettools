from django.db import IntegrityError
from django.shortcuts import render
from nettools.forms import AccessSwitchForm, AccessSwitchConfigForm, ZabbixForm, DeviceForm
from zabbix.zabbix_api_methods import zabbix_add_host
from django.core.mail import send_mail

from .generator import generator
from .models import AccessSwitch, AccessSwitchConfig, Device
from secrets.secrets import ZABBIX_EMAIL_DESTINATIONS, ZABBIX_EMAIL_SOURCE


def create_device(request):
    added = False
    r = False
    errors = []
    zabbix_enabled = False
    zabbix = ''

    if request.method == 'GET':
        if 'zabbix_enabled' in request.GET:
            zabbix_enabled = request.GET['zabbix_enabled']
    if request.method == 'POST':
        print('Info: Request method POST')
        device = DeviceForm(request.POST, prefix='device')

        if device.is_valid():
            print('Info: DEVICE Form is valid')
            cd_device = device.cleaned_data
            zabbix = ZabbixForm(request.POST, prefix='zabbix')
            if zabbix.is_valid():
                zabbix_enabled = True
                print('Info: Addition to Zabbix enabled')
                cd_zabbix = zabbix.cleaned_data
                r = zabbix_add_host(cd_device['hostname'], cd_device['ip'], cd_zabbix['group_name'],
                                    cd_zabbix['template_name'], cd_zabbix['snmp_community'], cd_zabbix['status'])
            else:
                print(zabbix.errors)
            try:
                if zabbix_enabled:
                    if r is True:
                        device.save()
                        added = True
                        print('Info: DEVICE data saved in Device DB. And DEVICE added in Zabbix')
                        message = 'Добавлено новое устройство:' + '\n\n' + str(cd_device['ip']) + ' ' + str(cd_device['hostname'] + '\n\n' + str(cd_device['description']))
                        send_mail('Zabbix. Новое устройство.', message, ZABBIX_EMAIL_SOURCE, ZABBIX_EMAIL_DESTINATIONS)
                    else:
                        print('Error: DEVICE data does not saved in Device DB because of error while adding in Zabbix')
                        errors.append(r.split('.')[1][2:] + ' in Zabbix')
                else:
                    device.save()
                    added = True
                    print('Info: DEVICE data saved in Device DB.')

            except Exception as e:
                print('Error: DEVICE data has not been saved in Device DB.')
                print('Error: {}'.format(e))
                errors.append(str(e))
        else:
            print('Error: DEVICE Form is not valid')
            print(device.errors)
    else:
        print('Info: Request method GET')
        device = DeviceForm(prefix='device')
        if zabbix_enabled:
            zabbix = ZabbixForm(prefix='zabbix')
    return render(request, 'create_device.html', {'device': device, 'zabbix': zabbix, 'errors': errors, 'added': added, 'zabbix_enabled': zabbix_enabled})


def generate_config(request):

    generated_config = ''
    if request.method == 'POST':
        print('Info: Request method POST')
        config = AccessSwitchConfigForm(request.POST, prefix='config')
        if config.is_valid():
            print('Info: CONFIG Forms are valid')
            cd_config = config.cleaned_data
            generated_config = generator(
                model=cd_config['model'],
                hostname=cd_config['hostname'],
                mgmt_vlan=cd_config['mgmt_vlan'],
                ip=cd_config['ip'],
                mask=cd_config['mask'],
                gw=cd_config['gw'],
                snmp_location=cd_config['snmp_location'],
                snmp_community=cd_config['snmp_community']
                )
        else:
            print('Error: CONFIG Form is not valid')
            print(config.errors)
    else:
        print('Info: Request method GET')
        config = AccessSwitchConfigForm(prefix='config')
    return render(request, 'generate_config.html',
                  {'config': config,
                   'generated_config': generated_config,
                   })


# def display_db(request):
#     last_ordering = ''
#     if 'o' in request.GET:
#         o = request.GET['o']
#         last_ordering = o
#         print(last_ordering)
#         devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by(o)
#         # devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by('hostname__purchase')
#     else:
#         devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by('hostname')
#     return render(request, 'list.html', {'devices': devices,'last_ordering': last_ordering})
def display_db(request):
    last_ordering = ''
    if 'del' in request.GET:
        d = request.GET['del']
        print('Info: Trying to delete "{}" from Device DB.'.format(d))
        try:
            Device.objects.filter(hostname=d).delete()
            print('Info: "{}" has been deleted from Device DB.'.format(d))
        except Exception as e:
            print('Error: "{}" can not be removed from Device DB.'.format(d))
            print('Error: {}'.format(e))
    if 'o' in request.GET:
        o = request.GET['o']
        last_ordering = o
        # print(last_ordering)
        devices = Device.objects.all().order_by(o)
        print('Info: Ordering by {}'.format(o))
        # devices = AccessSwitchConfig.objects.all().prefetch_related('hostname').order_by('hostname__purchase')
    elif 'q_po' in request.GET:
        search = request.GET['q_po']
        if search != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(po__icontains=search)
        else:
            devices = Device.objects.all().order_by('-addition_date')
            print('Info: Backup Default output.')
    elif 'q_model' in request.GET:
        search = request.GET['q_model']
        if search != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(model__icontains=search)
        else:
            devices = Device.objects.all().order_by('-addition_date')
            print('Info: Backup Default output.')
    elif 'q_ports' in request.GET:
        search = request.GET['q_ports']
        if search != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(ports__icontains=search)
        else:
            devices = Device.objects.all().order_by('-addition_date')
            print('Info: Backup Default output.')
    elif 'q_purchase' in request.GET:
        search = request.GET['q_purchase']
        if search != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(purchase__icontains=search)
        else:
            devices = Device.objects.all().order_by('-addition_date')
            print('Info: Backup Default output.')
    elif 'q' and 'q_ip' in request.GET:
        search = request.GET['q']
        search_ip = request.GET['q_ip']
        if search != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(hostname__icontains=search)
        elif search_ip != '':
            print('Info: Searching for "{}" in Device DB.'.format(search))
            devices = Device.objects.filter(ip__icontains=search_ip)
        else:
            devices = Device.objects.all().order_by('-addition_date')
            print('Info: Backup Default output.')
    else:
        devices = Device.objects.all().order_by('-addition_date')
        print('Info: Default output.')

    return render(request, 'list.html', {'devices': devices, 'last_ordering': last_ordering})
