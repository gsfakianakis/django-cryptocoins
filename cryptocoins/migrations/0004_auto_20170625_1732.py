# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coinmarket', '0003_coinportfolio_portfolioentries'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PortfolioEntries',
            new_name='CoinPortfolioEntries',
        ),
    ]
