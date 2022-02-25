from django.db import models
from django.forms import ModelForm


class Broker(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


class BrokerForm(ModelForm):
    prefix = 'broker'

    class Meta:
        model = Broker
        fields = ['name']
