# Generated by Django 4.0.2 on 2022-03-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cre_finance', '0007_building_cost_remove_loan_property_delete_property_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='cost',
            name='curve',
            field=models.CharField(choices=[('Straight line', 'Straight line'), ('Bell curve', 'Bell curve'), ('CSV input', 'CSV input')], default='Straight line', max_length=100),
        ),
        migrations.AddField(
            model_name='cost',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='cost',
            name='duration',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cost',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]