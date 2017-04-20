# -*- coding: utf-8 -*-
from django.db import models
import datetime

DEVICE_MODELS_CHOICES = (
    ('hp1910', 'HP 1910'),
    ('hp1920', 'HP 1920'),
    ('hp1950', 'HP 1950'),
    ('hp5120', 'HP 5120'),
    ('hp5500', 'HP 5500'),
    ('hp5800', 'HP 5800'),
    ('c2960', 'Cisco 2960'),
    ('c3560', 'Cisco 3560'),
    ('c3750', 'Cisco 3750'),
    ('c7600', 'Cisco 7604'),
    ('d1200', 'D-Link 1200'),
    ('d3200', 'D-Link 3200'),
    ('d3500', 'D-Link 3500'),
    ('rb750', 'Mikrotik RB750'),
    ('rb951', 'Mikrotik RB951'),
    ('m408', 'Moxa 408'),
    ('m6527', 'Moxa 6527'),
    ('q2800', 'Q-tech 2800'),
    ('q2900', 'Q-tech 2900'),
    ('q3900', 'Q-tech 3900'),
    ('srx110', 'Juniper SRX110'),
    ('srx210', 'Juniper SRX210'),
    ('srx340', 'Juniper SRX340'),
)

PORTS_NUMBER = (
    (8, '8'),
    (10, '10'),
    (16, '16'),
    (24, '24'),
    (28, '28'),
    (48, '48'),
    (52, '52'),
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
    # ('', ''),
    ('Лот 1272', 'Лот 1272'),
    ('ПАК АСДУ', 'ПАК АСДУ'),
)


class Device(models.Model):
    """
    Device template
    """
    hostname = models.CharField(max_length=30, verbose_name='Hostname', unique=True)
    ip = models.GenericIPAddressField(verbose_name='MGMT IP', unique=True)
    addition_date = models.DateField(verbose_name='Addition date', default=datetime.date.today)
    model = models.CharField(max_length=20, choices=sorted(DEVICE_MODELS_CHOICES, key=lambda tup: tup[1]), verbose_name='Model')
    ports = models.PositiveIntegerField(choices=PORTS_NUMBER, verbose_name='Ports number')
    po = models.CharField(max_length=10, choices=sorted(PO_LIST, key=lambda tup: tup[1]), verbose_name='PO name')
    purchase = models.CharField(max_length=20, choices=sorted(PURCHASES_LIST, key=lambda tup: tup[1]), blank=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        ordering = ['-addition_date']



class AccessSwitch(models.Model):
    """
    Access switch template
    """
    hostname = models.CharField(max_length=30, verbose_name='Hostname', unique=True)
    addition_date = models.DateField(verbose_name='Addition date')
    model = models.CharField(max_length=20, choices=DEVICE_MODELS_CHOICES, verbose_name='Model')
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
