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


# Create your models here.
ACQUISITION_COSTS = "Acquisition costs"
CONSTRUCTION_COSTS = "Construction costs"
PROFESSIONAL_FEES = "Professional fees"

TYPE_CHOICES = [
    (ACQUISITION_COSTS, "Acquisition costs"),
    (CONSTRUCTION_COSTS, "Construction costs"),
    (PROFESSIONAL_FEES, "Professional fees")
]


class Cost(models.Model):
    amount = models.FloatField()
    type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        default=CONSTRUCTION_COSTS)
    date_start = models.DateField(default=date.today)
    date_end = models.DateField(
        default=date.today)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'£{"{:,.0f}".format(self.amount)} - {self.type}'

    def get_absolute_url(self):
        return reverse('building:cost:detail', kwargs={'cost_pk': self.pk, 'building_pk': self.building.pk})

    @property
    def schedule(self):
        # date range
        date_range = payment_dates(self.date_start, self.date_end)

        # cost schedule
        months_duration = duration_months(self.date_start, self.date_end)
        costs_per_whole_month = self.amount / months_duration
        schedule = [costs_per_whole_month for period in range(
            len(list(date_range)))]
        if self.date_end is not None:
            schedule[0] = costs_per_whole_month * \
                day_to_month_frac(self.date_start)
            schedule[-1] = self.amount - sum(schedule[: -1])

        return pd.Series(data=schedule, index=date_range)


class CostForm(ModelForm):

    class Meta:
        model = Cost
        fields = ['amount', 'type', 'date_end', 'date_start']
        widgets = {
            'date_start': SelectDateWidget(),
            'date_end': SelectDateWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")

        if date_start > date_end:
            raise ValidationError("end date must be after start date")


CostFormSet = modelformset_factory(Cost, extra=2, form=CostForm)
