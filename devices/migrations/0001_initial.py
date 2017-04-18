# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 16:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessSwitch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=30, unique=True, verbose_name='Hostname')),
                ('addition_date', models.DateField(verbose_name='Addition date')),
                ('model', models.CharField(choices=[('hp1910', 'HP 1910'), ('hp1920', 'HP 1920'), ('hp1950', 'HP 1950'), ('hp5120', 'HP 5120'), ('hp5500', 'HP 5500'), ('hp5800', 'HP 5800'), ('c2960', 'Cisco 2960'), ('c3560', 'Cisco 3560'), ('c3750', 'Cisco 3750'), ('c7600', 'Cisco 7604'), ('d1200', 'D-Link 1200'), ('d3200', 'D-Link 3200'), ('d3500', 'D-Link 3500'), ('m408', 'Moxa 408'), ('m6527', 'Moxa 6527'), ('q2800', 'Q-tech 2800'), ('q2900', 'Q-tech 2900'), ('q3900', 'Q-tech 3900'), ('srx110', 'Juniper SRX110'), ('srx210', 'Juniper SRX210'), ('srx340', 'Juniper SRX340')], max_length=20, verbose_name='Model')),
                ('ports', models.PositiveIntegerField(choices=[(8, '8'), (10, '10'), (16, '16'), (24, '24'), (28, '28'), (48, '48'), (52, '52')], verbose_name='Ports number')),
                ('po', models.CharField(choices=[('BcES', 'ПО БцЭС'), ('BES', 'ПО БЭС'), ('CES', 'ПО ЦЭС'), ('IES', 'ПО ИЭС'), ('KES', 'ПО КЭС'), ('NES', 'ПО НЭС'), ('OES', 'ПО ОЭС'), ('SVES', 'ПО СВЭС'), ('SES', 'ПО СЭС'), ('UGES', 'ПО УГЭС'), ('TARGIN', 'Таргин')], max_length=10, verbose_name='PO name')),
                ('purchase', models.CharField(blank=True, choices=[('Лот 1272', 'Лот 1272'), ('ПАК АСДУ', 'ПАК АСДУ')], max_length=20)),
                ('description', models.TextField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ['-addition_date'],
            },
        ),
        migrations.CreateModel(
            name='AccessSwitchConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mgmt_vlan', models.PositiveIntegerField(verbose_name='MGMT Vlan')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='MGMT IP')),
                ('mask', models.GenericIPAddressField(verbose_name='MGMT mask')),
                ('gw', models.GenericIPAddressField(verbose_name='MGMT gateway')),
                ('snmp_location', models.CharField(max_length=50, verbose_name='SNMP Location')),
                ('hostname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='switch', to='devices.AccessSwitch')),
            ],
            options={
                'ordering': ['hostname'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=30, unique=True, verbose_name='Hostname')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='MGMT IP')),
                ('addition_date', models.DateField(default=datetime.date.today, verbose_name='Addition date')),
                ('model', models.CharField(choices=[('c2960', 'Cisco 2960'), ('c3560', 'Cisco 3560'), ('c3750', 'Cisco 3750'), ('c7600', 'Cisco 7604'), ('d1200', 'D-Link 1200'), ('d3200', 'D-Link 3200'), ('d3500', 'D-Link 3500'), ('hp1910', 'HP 1910'), ('hp1920', 'HP 1920'), ('hp1950', 'HP 1950'), ('hp5120', 'HP 5120'), ('hp5500', 'HP 5500'), ('hp5800', 'HP 5800'), ('srx110', 'Juniper SRX110'), ('srx210', 'Juniper SRX210'), ('srx340', 'Juniper SRX340'), ('m408', 'Moxa 408'), ('m6527', 'Moxa 6527'), ('q2800', 'Q-tech 2800'), ('q2900', 'Q-tech 2900'), ('q3900', 'Q-tech 3900')], max_length=20, verbose_name='Model')),
                ('ports', models.PositiveIntegerField(choices=[(8, '8'), (10, '10'), (16, '16'), (24, '24'), (28, '28'), (48, '48'), (52, '52')], verbose_name='Ports number')),
                ('po', models.CharField(choices=[('BES', 'ПО БЭС'), ('BcES', 'ПО БцЭС'), ('IES', 'ПО ИЭС'), ('KES', 'ПО КЭС'), ('NES', 'ПО НЭС'), ('OES', 'ПО ОЭС'), ('SVES', 'ПО СВЭС'), ('SES', 'ПО СЭС'), ('UGES', 'ПО УГЭС'), ('CES', 'ПО ЦЭС'), ('TARGIN', 'Таргин')], max_length=10, verbose_name='PO name')),
                ('purchase', models.CharField(blank=True, choices=[('Лот 1272', 'Лот 1272'), ('ПАК АСДУ', 'ПАК АСДУ')], max_length=20)),
                ('description', models.TextField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ['-addition_date'],
            },
        ),
    ]
