from django import template
import pandas as pd
from cre_finance.utilities import json_to_df

register = template.Library()


@register.filter
def to_percent(number, digits):
    return "{0:.{digits}%}".format(number, digits=digits)


@register.filter
def pc_to_percent(number, digits):
    return "{0:.{digits}%}".format(number/100, digits=digits)


@register.filter
def to_multiple(number, digits):
    return "{:,.{digits}f}x".format(number, digits=digits)


@register.filter
def df_json_to_html(df_json):
    df = json_to_df(df_json)
    return df.to_html()


@register.filter
def ds_to_html(ds):
    return ds.to_frame().to_html(header=False)


@register.filter
def df_to_html(df):
    return df.to_html()


@register.filter
def df_json_empty(df_json):
    return pd.read_json(df_json).empty
