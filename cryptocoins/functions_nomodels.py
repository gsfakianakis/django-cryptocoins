import urllib.request, json

Coin_DATA_API = 1 # 1 = coinmarketcap.com

def Coin_Data_Api_Call(coinmarketcap_com_id = None):
    if Coin_DATA_API == 1:
        data = coinmarketcap_com_call(coinmarketcap_com_id)
    if Coin_DATA_API == 2:
        pass    

    return data

def coinmarketcap_com_call(coinmarketcap_com_id = None):
    if coinmarketcap_com_id == 'all_coins' or coinmarketcap_com_id is None:
        url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/")
        data = json.loads(url.read().decode())
        return data
    else:
        url = urllib.request.urlopen("http://api.coinmarketcap.com/v1/ticker/" + coinmarketcap_com_id +"/")
        data = json.loads(url.read().decode())
        return data[0]
