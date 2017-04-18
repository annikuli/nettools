from django.db import models
from devices.models import Device
# Create your models here.


class Vsi(models.Model):
    name = models.CharField(max_length=10, unique=True)
    vsi_id = models.IntegerField(unique=True)
    switch = models.ManyToManyField(Device)
    description = models.CharField(max_length=200, blank=True)
    addition_date = models.DateField(verbose_name='Addition date')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']