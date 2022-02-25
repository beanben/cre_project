from django.db import models
from .sponsor import Sponsor
from .property import Property
from .broker import Broker
from django.forms import ModelForm
import pdb


class Deal(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.SET_NULL)
    property = models.ForeignKey(
        Property, null=True, blank=True, on_delete=models.SET_NULL)
    broker = models.ForeignKey(
        Broker, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name if self.name else f'{self.sponsor} - {self.property}'
        return super().save(*args, **kwargs)


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = [
            'sponsor',
            'property',
            'broker'
        ]
