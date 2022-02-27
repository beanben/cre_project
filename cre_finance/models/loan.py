from django.db import models
from .sponsor import Sponsor
from .building import Building
from .broker import Broker
from django.forms import ModelForm
import pdb


class Loan(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.SET_NULL)
    building = models.ForeignKey(
        Building, null=True, blank=True, on_delete=models.SET_NULL)
    broker = models.ForeignKey(
        Broker, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.name = self.name if self.name else f'{self.sponsor} - {self.building}'
