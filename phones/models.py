from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['organization']