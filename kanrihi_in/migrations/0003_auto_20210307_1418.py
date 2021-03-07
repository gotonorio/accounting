# Generated by Django 3.1.7 on 2021-03-07 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanrihi_in', '0002_kanrihi_income_comment'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='kanrihi_income',
            constraint=models.UniqueConstraint(fields=('ki', 'master'), name='kanrihi_in_unique'),
        ),
    ]