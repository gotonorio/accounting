# Generated by Django 3.0.7 on 2020-06-16 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequense', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_koujitype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('koujitype', models.CharField(max_length=256)),
                ('sequense', models.IntegerField()),
                ('live', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rireki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2009)),
                ('koujimei', models.CharField(max_length=256)),
                ('cost', models.BigIntegerField()),
                ('account_type', models.CharField(choices=[('管理費会計', '管理費会計'), ('修繕費会計', '修繕費会計'), ('駐車場会計', '駐車場会計')], max_length=16)),
                ('quotation_id', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('constractor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shuuzenhi_out.Constractor')),
                ('koujitype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shuuzenhi_out.Master_koujitype')),
            ],
        ),
    ]
