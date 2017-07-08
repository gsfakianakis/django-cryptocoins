=====
CryptoCoins
=====

CryptoCoins is a simple Django app to keep an overview of your cryptocoins.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "cryptocoins" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cryptocoins',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^cryptocoins/', include('cryptocoins.urls')),

3. Create the cryptocoins models::

    python manage.py migrate

4. Run::

    python manage.py J1_Update_Coins --import-all

to import all cryptocoins from coinmarketcap.com.

As an alternative you can run::

    python manage.py J1_Update_Coins --import-only BTC,ETH,STORJ

to import only these cryptocoins

5. Run::

    python manage.py J1_Update_Coins

or visit::

    http://127.0.0.1:8000/cryptocoins/coins/update_all/

to update the prices of imported cyptocoins
