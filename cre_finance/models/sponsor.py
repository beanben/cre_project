from django.db import models
from django.forms import ModelForm


class Sponsor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SponsorForm(ModelForm):
    prefix = 'sponsor'

    class Meta:
        model = Sponsor
        fields = ['name']
