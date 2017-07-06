import urllib.request, json


def coinmarketcap_com_call_coin(coinmarketcap_com_id):
    url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/" + coinmarketcap_com_id +"/")
    data = json.loads(url.read().decode())
    return data[0]


def coinmarketcap_com_call_All():
    url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/")
    data = json.loads(url.read().decode())
    return data

def coinmarketcap_com_data_to_obj(thejson):
    return obj
