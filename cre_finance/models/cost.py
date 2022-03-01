from django.db import models
from django.forms import ModelForm, SelectDateWidget
from django.urls import reverse
from django.core.exceptions import ValidationError
from .building import Building
from cre_finance.utilities import payment_dates, duration_months, day_to_month_frac
import pandas as pd
from datetime import date
import json
from django.forms import modelformset_factory


class Cost(models.Model):
    # COSTS CHOICES
    ACQUISITION_COSTS = "Acquisition costs"
    CONSTRUCTION_COSTS = "Construction costs"
    PROFESSIONAL_FEES = "Professional fees"

    TYPE_CHOICES = [
        (ACQUISITION_COSTS, "Acquisition costs"),
        (CONSTRUCTION_COSTS, "Construction costs"),
        (PROFESSIONAL_FEES, "Professional fees")
    ]

    # CURVE CHOICES
    STRAIGHT_LINE = "Straight line"
    BELL_CURVE = "Bell curve"
    CSV_INPUT = "CSV input"

    TYPE_CURVES = [
        (STRAIGHT_LINE, "Straight line"),
        (BELL_CURVE, "Bell curve"),
        (CSV_INPUT, "CSV input")
    ]

    category = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        default=CONSTRUCTION_COSTS)
    description = models.CharField(blank=True, max_length=100)
    amount = models.FloatField(blank=True, null=True)
    date_start = models.DateField(default=date.today)
    duration = models.FloatField()
    date_end = models.DateField(default=date.today)
    curve = models.CharField(
        max_length=100,
        choices=TYPE_CURVES,
        default=STRAIGHT_LINE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'£{"{:,.0f}".format(self.amount)} - {self.type}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class CostForm(ModelForm):

    class Meta:
        model = Cost
        fields = [
            'category',
            'description',
            'amount',
            'date_start',
            'duration',
            'date_end',
            'curve'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


CostFormSet = modelformset_factory(Cost, extra=2, form=CostForm)
