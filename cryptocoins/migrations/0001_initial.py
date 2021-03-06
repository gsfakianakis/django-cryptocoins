# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('balance', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('balance_usd', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('symbol', models.CharField(default='...', max_length=30, verbose_name='Symbol')),
                ('coinmarketcap_com_id', models.CharField(default='...', max_length=25, verbose_name='Symbol or id in coinmarketcap_com API')),
                ('price_btc', models.DecimalField(decimal_places=30, default=0, max_digits=40)),
                ('price_usd', models.DecimalField(decimal_places=30, default=0, max_digits=40)),
                ('capitalization', models.DecimalField(decimal_places=2, default=0, max_digits=22)),
                ('market_supply', models.DecimalField(decimal_places=2, default=0, max_digits=22)),
                ('total_supply', models.DecimalField(decimal_places=2, default=0, max_digits=22)),
                ('price_updated', models.DateTimeField(blank=True, null=True)),
                ('last_update_try', models.DateTimeField(default=django.utils.timezone.now)),
                ('blockchain', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='cryptocoins.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='CoinPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cost_usd', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('balance_usd', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('balance_euros', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('profit', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('profit_percent', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoinPortfolioEntry',
            fields=[
                ('balance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cryptocoins.Balance')),
                ('public_address', models.CharField(max_length=150, verbose_name='Public Key')),
                ('buy_price_usd', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('profit', models.DecimalField(decimal_places=10, default=0, max_digits=40)),
                ('profit_percent', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='cryptocoins.CoinPortfolio')),
            ],
            bases=('cryptocoins.balance',),
        ),
        migrations.AddField(
            model_name='balance',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptocoins.Coin'),
        ),
    ]
