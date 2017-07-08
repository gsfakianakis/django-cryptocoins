from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from optparse import make_option
# import urllib2
#import requests,sys,random
# import xml.etree.ElementTree as ET
# import pytz,shutil,datetime,os,time
#from django.utils.dateparse import parse_datetime
from mycoinfolio.settings import *
from cryptocoins.functions_nomodels import *
from cryptocoins.models import *


class Command(BaseCommand):
    help = 'Updates coins and prices'

    def add_arguments(self, parser):
        # This is an optional argument
        parser.add_argument(
            '--import-all',  # argument flag
            action='store_true',  # action to take, stores true if present
            dest='import',  # argument name
            default=False,  # it is false by default
            help="Import New Coins"  # a help message
        )
        parser.add_argument(
            '--import-only',  # argument flag
            action='store',
            #type='float',
            dest='import_list',  # argument name
            default=False,  # it is false by default
            help="Import New Coins"  # a help message
        )

    def handle(self, *args, **options):
        Import_New_Coins = options['import']

        if options['import_list']:
            Import_List = options['import_list'].lower().split(',');

        New_Added = 0
        Updated = 0
        data_all = Coin_Data_Api_Call()
        print(len(data_all))

        for data in data_all:
            ccid = data['id']
            csymbol = data['symbol']

            exist = 1
            try:
                cn = Coin.objects.get(coinmarketcap_com_id = ccid)
            except:
                exist = 0

            if exist == 1:
                cn.update_price(data)
                Updated = Updated + 1
                print("Updated: " + data['name'])
            elif exist == 0 and (Import_New_Coins or (csymbol.lower() in Import_List) ):
                New_Added = New_Added + 1
                cn = Coin.objects.create(name = data['name'], symbol = data['symbol'], coinmarketcap_com_id = data['id'])
                cn.update_price(data)
                print("New Added: " + data['name'])


        self.stdout.write('        ')
        self.stdout.write('Total..' + str(len(data_all)))
        self.stdout.write('Updated..' + str(Updated) + '\n' )
        self.stdout.write('New Added..' + str(New_Added) + '\n')
        self.stdout.write('        ')
        self.stdout.write('Done...')
