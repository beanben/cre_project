from django.db import models
from django.urls import reverse
from django.forms import ModelForm, CharField
from django import forms
import pandas as pd


class Building(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('building-detail', kwargs={'pk': self.pk})

    @property
    def development_schedule(self):
        df = pd.DataFrame()
        costs = self.cost_set.all()

        if len(costs) != 0:
            df = pd.concat(
                [cost.schedule for cost in costs],
                axis=1,
                keys=[cost.type for cost in costs]
            ).fillna(0)

            # add a total.
            df["total"] = df.sum(axis=1)

            # name index column
            df.index.name = "Payment date"

        return df


class BuildingForm(ModelForm):

    class Meta:
        model = Building
        fields = ['name', 'value']
