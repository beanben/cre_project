# Generated by Django 4.0.2 on 2022-02-19 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cre_finance', '0006_property_postcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='city',
        ),
    ]