# Generated by Django 4.0.2 on 2022-02-21 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cre_finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.CharField(max_length=100),
        ),
    ]