from django.db import models
from django import forms
from django.forms import ModelForm
from django.urls import reverse
from cre_finance.utilities import date_range, duration_months, ds_days, json_to_df, df_to_json, update_df, timeit
from .building import Building
from datetime import datetime, date
from pyxirr import xirr as py_xirr
import pandas as pd
import numpy as np
import json
import pdb


class Loan(models.Model):
    # class parametres
    facility_columns = [
        "funding date",
        "days btwn periods",
        "opening balance",
        "arrangement fee",
        "interest",
        "capital",
        "non-utilisation fee",
        "repayment",
        "closing balance",
        "exit fee",
        "cashflow",
        "facility used cumul"
    ]
    funding_columns = [
        "funding date",
        "funding required",
        "equity capital funding",
        "debt capital funding"
    ]
    max_headroom = 50000
    round_to = 50000

    # fields initally defined
    name = models.CharField(max_length=100)
    arrangement_fee_pct = models.FloatField(default=0)
    interest_pct = models.FloatField(default=0)
    non_utilisation_fee_pct = models.FloatField(default=0)
    exit_fee_pct = models.FloatField(default=0)
    ltv_covenant = models.FloatField(default=0)
    ltc_covenant = models.FloatField(default=0)
    building = models.OneToOneField(
        Building,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # fields defined based on building instance values
    start_date = models.DateField(default=date.today)
    maturity_date = models.DateField(default=date.today)

    # calculated fields
    facility_schedule = models.JSONField(default=dict)
    funding_schedule = models.JSONField(default=dict)
    equity_required = models.FloatField(default=0)
    facility_amount = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('loan:detail', kwargs={'loan_pk': self.pk})

    @property
    def funding_required(self):
        if self.building is not None:
            return self.building.development_schedule["total"]
        else:
            return pd.Series()

    @property
    def capital(self):
        return json_to_df(self.facility_schedule).get("capital").sum()

    @property
    def term_months(self):
        return duration_months(self.start_date, self.maturity_date)

    @property
    def profit(self):
        return json_to_df(self.facility_schedule)["cashflow"].sum()

    @property
    def xirr(self):
        schedule = json_to_df(self.facility_schedule)
        dates = schedule["funding date"]
        amounts = schedule["cashflow"]
        return py_xirr(dates, amounts)
        # return 0

    @property
    def em(self):
        return (self.capital + self.profit) / self.capital

    @property
    def coc(self):
        return ((self.em - 1) / self.term_months) * 12

    @property
    def repayment(self):
        return abs(json_to_df(self.facility_schedule)["repayment"].sum())

    @property
    def arrangement_fee(self):
        return json_to_df(self.facility_schedule)["arrangement fee"].sum()

    @property
    def interest(self):
        return json_to_df(self.facility_schedule)["interest"].sum()

    @property
    def non_utilisation_fee(self):
        return json_to_df(self.facility_schedule)["non-utilisation fee"].sum()

    @property
    def finance_costs_capitalised(self):
        finance_costs_capitalised = [
            self.arrangement_fee,
            self.interest,
            self.non_utilisation_fee
        ]
        return sum(finance_costs_capitalised)

    @property
    def total_funded_costs(self):
        total_funded_costs = [
            self.finance_costs_capitalised,
            self.capital
        ]
        return sum(total_funded_costs)

    @property
    def headroom(self):
        return self.facility_amount - self.total_funded_costs

    @property
    def total_hard_costs(self):
        return self.funding_required.sum()

    @property
    def total_fundable_costs(self):
        return self.finance_costs_capitalised + self.total_hard_costs

    @property
    def ltv(self):
        return self.facility_amount / self.building.value

    @property
    def ltc(self):
        return self.facility_amount / self.total_fundable_costs

    def facility_schedule__refresh(self):
        schedule = json_to_df(self.facility_schedule)

        # reset values to zero
        re_set_columns = [col for col in list(schedule.columns) if col not in [
            "days btwn periods", "capital", "funding date"]]
        schedule[re_set_columns] = 0

        # arrangement fee
        np_af = np.zeros(len(schedule))
        np_af[0] = self.arrangement_fee_pct/100 * self.facility_amount
        schedule["arrangement fee"] = np_af

        # exit fee
        np_ef = np.zeros(len(schedule))
        np_ef[-1] = self.exit_fee_pct/100 * self.facility_amount
        schedule["exit fee"] = np_ef

        # initial values
        closing_balance = 0
        used_cumul = 0

        for index, row in schedule.iterrows():
            days = row["days btwn periods"]
            capital = row["capital"]

            # opening balance
            schedule.at[index, "opening balance"] = closing_balance

            # interest
            schedule.at[index,
                        "interest"] = round(self.interest_pct/100 * schedule.at[index, "opening balance"] * days / 365, 2)

            # non utilisation fee
            facility_used_cumul_previous = used_cumul
            schedule.at[index,
                        "non-utilisation fee"] = round(self.non_utilisation_fee_pct/100 * max(0, self.facility_amount - facility_used_cumul_previous) * days / 365, 2)

            # facility used cumul
            facility_used = sum([schedule.at[index, "arrangement fee"],
                                 schedule.at[index, "interest"],
                                 capital,
                                 schedule.at[index, "non-utilisation fee"]])
            used_cumul = facility_used + facility_used_cumul_previous
            schedule.at[index, "facility used cumul"] = used_cumul

            # repayment and exit fee
            if index == len(schedule.index)-1:
                schedule.at[index, "repayment"] = - sum([
                    schedule.at[index, "opening balance"],
                    schedule.at[index, "interest"],
                    capital,
                    schedule.at[index, "non-utilisation fee"]
                ])

            # closing balance
            closing_balance = sum([
                schedule.at[index, "opening balance"],
                schedule.at[index, "arrangement fee"],
                schedule.at[index, "interest"],
                capital,
                schedule.at[index, "non-utilisation fee"],
                schedule.at[index, "repayment"]
            ])
            schedule.at[index, "closing balance"] = closing_balance

        # cashflow
        schedule["cashflow"] = - schedule["capital"] - \
            schedule["repayment"] - schedule["exit fee"]

        # convert schedule to json
        self.facility_schedule = df_to_json(schedule)

    def facility_schedule__initialise(self):
        if len(self.facility_schedule) != 0:
            schedule = pd.DataFrame(columns=self.facility_columns)
        else:
            schedule = pd.DataFrame.from_dict(
                self.facility_schedule,
                orient='index',
                columns=self.facility_columns)

        # funding dates to take into account standard of end of month for payment of interest
        schedule["funding date"] = date_range(
            self.start_date, self.maturity_date)

        # set index of schedule as funding dates, to be able to combine with the Series funding_required
        schedule.index = schedule["funding date"]

        # define total funding required
        schedule["capital"] = self.funding_required

        # reset index such that index shows period number
        schedule.reset_index(inplace=True, drop=True)
        schedule.index.name = "period"

        # days between periods
        schedule["days btwn periods"] = ds_days(schedule, "funding date")

        schedule.fillna(0, inplace=True)

        schedule["facility used cumul"] = schedule["capital"].cumsum()

        # convert schedule to json
        self.facility_schedule = df_to_json(schedule)

        # refresh finance costs now that funding required is defined
        self.facility_schedule__refresh()

    def funding_schedule__refresh(self):
        schedule = json_to_df(self.funding_schedule)
        equity = self.equity_required

        # initialise funders invested amount
        schedule["equity capital funding"] = 0
        schedule["debt capital funding"] = 0

        # equity capital funding
        schedule["equity capital funding"] = np.where(
            schedule["funding required"].cumsum() <= equity,
            schedule["funding required"],
            0)

        # equity funding in period where equity is last available
        index_last = np.where(
            schedule["equity capital funding"] == 0)[0][0]
        schedule.at[index_last, "equity capital funding"] = equity - \
            schedule["equity capital funding"].sum()

        # debt capital funding
        schedule["debt capital funding"] = schedule["funding required"] - \
            schedule["equity capital funding"]

        # update facility_schedule with the new spread of costs
        df_facility_schedule = update_df(
            df_to_update=json_to_df(self.facility_schedule),
            df_updating=schedule,
            col_to_update="capital",
            col_updating="debt capital funding",
            join_on="funding date"
        )

        self.funding_schedule = df_to_json(schedule)
        self.facility_schedule = df_to_json(df_facility_schedule)
        self.facility_schedule__refresh()

    def equity_required__update(self, amount):
        self.equity_required = self.equity_required + amount
        self.funding_schedule__refresh()
        self.facility_schedule__refresh()

    def facility_amount__initialise(self):
        self.facility_schedule__refresh()
        self.facility_amount = self.repayment
        self.equity_required = self.equity_required - self.headroom
        self.funding_schedule__refresh()
        while int(self.headroom) != 0:
            self.facility_schedule__refresh()
            self.facility_amount = self.repayment
            self.equity_required = self.equity_required - self.headroom
            self.funding_schedule__refresh()

        self.facility_schedule__refresh()

    def funding_schedule__initialise(self):
        if len(self.funding_schedule) != 0:
            schedule = pd.DataFrame(columns=self.funding_columns)
        else:
            schedule = pd.DataFrame.from_dict(
                self.funding_schedule,
                orient='index',
                columns=self.funding_columns)

        schedule["funding required"] = self.funding_required
        schedule["funding date"] = schedule.index

        # reset index such that index shows period number
        schedule.reset_index(inplace=True, drop=True)
        schedule.index.name = "period"

        # all funding initially from debt
        schedule = update_df(
            df_to_update=schedule,
            df_updating=json_to_df(self.facility_schedule),
            col_to_update="debt capital funding",
            col_updating="capital",
            join_on="funding date"
        )

        # set values of columns to zero
        schedule.fillna(0, inplace=True)

        self.funding_schedule = df_to_json(schedule)

    def facility_capped(self):
        return min(self.ltv_covenant/100 * self.building.value, self.ltc_covenant/100 * self.total_fundable_costs)

    def facility_amount__size(self):
        # resize loan and define equity required based on loan leverage covenants
        while int(self.headroom) != 0:
            self.facility_amount = self.facility_capped()
            self.facility_schedule__refresh()
            self.equity_required__update(- self.headroom)

    def facility_amount__round(self):
        self.facility_amount = int(
            self.facility_amount / self.round_to) * self.round_to
        self.facility_schedule__refresh()
        while int(self.headroom) != 0:
            self.equity_required__update(- self.headroom)
        if self.headroom < 0:
            self.equity_required__update(self.headroom)

    def add_headroom(self):
        while int(self.headroom) != self.max_headroom:
            self.equity_required__update(self.max_headroom - self.headroom)

    @timeit
    def calculate(self):
        self.facility_amount = 0
        self.equity_required = 0
        self.facility_schedule__initialise()
        self.funding_schedule__initialise()
        self.facility_amount__initialise()

        # assign collateral to the loan and resize loan based on loan  covenants
        self.facility_amount = self.facility_capped()
        self.equity_required__update(- self.headroom)

        # size facility, within the covenant parameters
        self.facility_amount__size()

        # round facility such that the headroom is below or equal to loan.max_headroom
        self.facility_amount__round()

        # add headroom as defined in class parameter
        self.add_headroom()

        self.save()


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['name',
                  'arrangement_fee_pct',
                  'interest_pct',
                  'non_utilisation_fee_pct',
                  'exit_fee_pct',
                  'ltv_covenant',
                  'ltc_covenant',
                  'building']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.building is not None:
            development_schedule = instance.building.development_schedule
            instance.start_date = min(development_schedule.index)
            instance.maturity_date = max(development_schedule.index)
        if commit:
            instance.save()
        return instance


class LoanUpdateForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['name',
                  'arrangement_fee_pct',
                  'interest_pct',
                  'non_utilisation_fee_pct',
                  'exit_fee_pct',
                  'ltv_covenant',
                  'ltc_covenant',
                  'building']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.calculate()
        if commit:
            instance.save()
        return instance
