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

3. Run `python manage.py migrate` to create the cryptocoins models.
