# Generated by Django 3.1.7 on 2021-03-07 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuuzenhi_in', '0003_auto_20210207_1427'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='shuuzenhi_income',
            constraint=models.UniqueConstraint(fields=('ki', 'master'), name='shuuzenhi_in_unique'),
        ),
    ]