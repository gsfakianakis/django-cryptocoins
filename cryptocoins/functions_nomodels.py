import urllib.request, json
from django.utils import timezone
import datetime
import pytz
from decimal import Decimal as dm

Coin_DATA_API = 1 # 1 = coinmarketcap.com

def Coin_Data_Api_Call(coinmarketcap_com_id = None):
    if Coin_DATA_API == 1:
        data = coinmarketcap_com_call(coinmarketcap_com_id)
    if Coin_DATA_API == 2:
        pass

    return data

def coinmarketcap_com_call(coinmarketcap_com_id = None):
    if coinmarketcap_com_id == 'all_coins' or coinmarketcap_com_id is None:
        url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/?limit=10000")
        data = json.loads(url.read().decode())
        return data
    else:
        try:
            url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/" + coinmarketcap_com_id +"/")
        except:
            data = None
            return data

        data = json.loads(url.read().decode())
        return data[0]


##############

def Get_USD_Euro_Rate(date = None):
    if date is None:
        url = urllib.request.urlopen("http://data.fixer.io/api/latest?symbols=USD&access_key=dd70cde15cf1340b4e8c61abf36bf3a8")
        data = json.loads(url.read().decode())
    else:
        api_url = "http://data.fixer.io/api/" + date.strftime("%Y-%m-%d") + "?symbols=USD&access_key=dd70cde15cf1340b4e8c61abf36bf3a8"
        url = urllib.request.urlopen(api_url)
        data = json.loads(url.read().decode())

    date_String = (data["date"] + "T16:00" ) # 4PM CET
    tmp_time = datetime.datetime.strptime(date_String, '%Y-%m-%dT%H:%M')
    the_date = tmp_time.replace(tzinfo=pytz.timezone('CET'))

    return dm(data["rates"]["USD"]), the_date
