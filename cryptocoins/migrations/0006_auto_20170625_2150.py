# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinmarket', '0005_auto_20170625_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinportfolioentry',
            name='public_address',
            field=models.CharField(max_length=150, verbose_name='Public Key'),
        ),
    ]
