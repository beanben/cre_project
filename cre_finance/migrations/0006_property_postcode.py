# Generated by Django 4.0.2 on 2022-02-18 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cre_finance', '0005_auto_20220213_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='postcode',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]