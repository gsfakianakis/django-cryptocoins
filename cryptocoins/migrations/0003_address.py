# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-28 14:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptocoins', '0002_auto_20170708_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('balance', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('balance_usd', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('diff_balance', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptocoins.Coin')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
