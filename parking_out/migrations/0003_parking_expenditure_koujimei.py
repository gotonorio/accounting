# Generated by Django 3.1.7 on 2021-02-26 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_out', '0002_auto_20200913_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking_expenditure',
            name='koujimei',
            field=models.CharField(default='', max_length=256),
        ),
    ]
