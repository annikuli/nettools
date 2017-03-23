from django.shortcuts import render
from nettools.forms import AccessSwitchForm, AccessSwitchConfigForm
from .models import AccessSwitch, AccessSwitchConfig
from django.db import IntegrityError

def generate_config(request):
    device_error = False
    if request.method == 'POST':
        device = AccessSwitchForm(request.POST, prefix='device')
        config = AccessSwitchConfigForm(request.POST, prefix='config')

        if device.is_valid() and config.is_valid():
            cd = device.cleaned_data
            cd2 = config.cleaned_data
            device_data = AccessSwitch(
                hostname=cd['hostname'],
                addition_date=cd['addition_date'],
                model=cd['model'],
                ports=cd['ports'],
                po=cd['po'],
                purchase=cd['purchase'],
                description=cd['description']
                )
            config_data = AccessSwitchConfig(
                hostname=device_data,
                mgmt_vlan = cd2['mgmt_vlan'],
                ip = cd2['ip'],
                mask = cd2['mask'],
                gw = cd2['gw'],
                snmp_location = cd2['snmp_location']
            )
            try:
                device_data.save()
                config_data.save()
            except IntegrityError as e:
                device_error = e
        else:
            print(device.errors)
            print(config.errors)
    else:
        device = AccessSwitchForm(prefix='device')
        config = AccessSwitchConfigForm(prefix='config')
    return render(request, 'generate_config.html', {'device': device, 'config': config, 'device_error': device_error})
