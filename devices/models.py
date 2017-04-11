# -*- coding: utf-8 -*-
from django.db import models


ACCESS_MODELS_CHOICES = (
    ('hp1910', 'HP 1910'),
)

PORTS_NUMBER = (
    (8, '8'),
    (16, '16'),
    (24, '24'),
)

PO_LIST = (
    ('BcES', 'ПО БцЭС'),
    ('BES', 'ПО БЭС'),
    ('CES', 'ПО ЦЭС'),
    ('IES', 'ПО ИЭС'),
    ('KES', 'ПО КЭС'),
    ('NES', 'ПО НЭС'),
    ('OES', 'ПО ОЭС'),
    ('SVES', 'ПО СВЭС'),
    ('SES', 'ПО СЭС'),
    ('UGES', 'ПО УГЭС'),
    ('TARGIN', 'Таргин')
)

PURCHASES_LIST = (
    ('', ''),
    ('1272', 'Лот 1272'),
    ('pakasdu', 'ПАК АСДУ'),
)


class AccessSwitch(models.Model):
    """
    Access switch template
    """
    hostname = models.CharField(max_length=30, verbose_name='Hostname', unique=True)
    addition_date = models.DateField(verbose_name='Addition date')
    model = models.CharField(max_length=20, choices=ACCESS_MODELS_CHOICES, verbose_name='Model')
    ports = models.PositiveIntegerField(choices=PORTS_NUMBER, verbose_name='Ports number')
    po = models.CharField(max_length=10, choices=PO_LIST, verbose_name='PO name')
    purchase = models.CharField(max_length=20, choices=PURCHASES_LIST, blank=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        ordering = ['-addition_date']


class AccessSwitchConfig(models.Model):
    """
    Configuration parameters for access switches
    """
    hostname = models.ForeignKey(AccessSwitch, related_name='switch')
    mgmt_vlan = models.PositiveIntegerField(verbose_name='MGMT Vlan')
    ip = models.GenericIPAddressField(verbose_name='MGMT IP', unique=True)
    mask = models.GenericIPAddressField(verbose_name='MGMT mask')
    gw = models.GenericIPAddressField(verbose_name='MGMT gateway')
    snmp_location = models.CharField(max_length=50, verbose_name='SNMP Location')

    def __str__(self):
        return str(self.hostname)

    class Meta:
        ordering = ['hostname']
