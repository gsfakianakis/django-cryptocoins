from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
# import urllib2
#import requests,sys,random
# import xml.etree.ElementTree as ET
# import pytz,shutil,datetime,os,time
#from django.utils.dateparse import parse_datetime
from mycoinfolio.settings import *
from coinmarket.functions_nomodels import *
from coinmarket.models import *

# xml_time_zone = 'Europe/Berlin'

def xstr(s):
    if s is None:
        return ''
    return str(s)

def adv_float(x):
    if x is None:
        return None
    else:
        return float(x)


class Command(BaseCommand):
    help = 'Updates coins and prices'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        New_Added = 0
        Updated = 0
        data_all = coinmarketcap_com_call_All()
        print(len(data_all))

        for data in data_all:
            ccid = data['id']

            exist = 1
            try:
                cn = Coin.objects.get(coinmarketcap_com_id = ccid)
            except:
                exist = 0

            if exist == 1:
                cn.update_prices(data)
                Updated = Updated + 1
                print("Updated: " + data['name'])
            elif exist == 0 and ccid == 'monaco':
                New_Added = New_Added + 1
                cn = Coin.objects.create(name = data['name'], symbol = data['symbol'], coinmarketcap_com_id = data['id'])
                cn.update_prices(data)
                print("New Added: " + data['name'])


            # if ccid == 'storj' or ccid == 'storjcoin-x':
            #     print(data['id'])

        self.stdout.write('        ')
        self.stdout.write('Updated..' + str(Updated))
        self.stdout.write('New Added..' + str(New_Added))
        self.stdout.write('        ')
        self.stdout.write('Done...')
