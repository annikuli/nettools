from django import forms
from zabbix.zabbix_api_methods import zabbix_list_groups
from django.forms.extras.widgets import SelectDateWidget
from devices.models import ACCESS_MODELS_CHOICES, PORTS_NUMBER, PO_LIST, PURCHASES_LIST


TEMPLATES = [('juniper', 'Juniper'),
             ('cisco', 'Cisco'),
             ('cisco asa', 'Cisco ASA'),
             ('dlink', 'Dlink'),
             ('juniper', 'Juniper'),
             ('hp1910', 'hp1910'),
             ('hp1920', 'hp1920'),
             ('hp1950', 'hp1950'),
             ('hp5120', 'hp5120'),
             ('hp5500', 'hp5500'),
             ('hp5800', 'hp5800'),
             ('mikrotik', 'Mikrotik'),
             ('moxa', 'Moxa'),
             ('ping loss', 'Ping'),
             ('qtech', 'Qtech'),
             ]


class DeviceForm(forms.Form):
    hostname = forms.CharField(max_length=30)
    ip_address = forms.GenericIPAddressField()
    group_name = forms.MultipleChoiceField(
        choices=zabbix_list_groups(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    template_name = forms.ChoiceField(choices=TEMPLATES, widget=forms.Select(attrs={'class': 'form-control'}))
    snmp_community = forms.CharField(max_length=30, required=False)


class AccessSwitchForm(forms.Form):
    hostname = forms.CharField(max_length=30)
    addition_date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    model = forms.ChoiceField(choices=ACCESS_MODELS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    ports = forms.ChoiceField(choices=PORTS_NUMBER, widget=forms.Select(attrs={'class': 'form-control'}))
    po = forms.ChoiceField(choices=PO_LIST, widget=forms.Select(attrs={'class': 'form-control'}))
    purchase = forms.ChoiceField(
        choices=PURCHASES_LIST,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(required=False, widget=forms.Textarea)


class AccessSwitchConfigForm(forms.Form):
    mgmt_vlan = forms.IntegerField(max_value=4096)
    ip = forms.GenericIPAddressField()
    mask = forms.GenericIPAddressField()
    gw = forms.GenericIPAddressField()
    snmp_location = forms.CharField(max_length=50)
