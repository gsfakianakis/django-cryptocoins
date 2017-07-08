from django.db import models
from django.utils import timezone
from .functions_nomodels import Coin_Data_Api_Call
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Coin(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField('Symbol', default='...',max_length = 30)
    coinmarketcap_com_id = models.CharField('Symbol or id in coinmarketcap_com API', default='...',max_length = 25)
    blockchain = models.ForeignKey('self',blank=True, null=True,default=None)

    price_btc = models.DecimalField(max_digits=40, decimal_places=30,default=0)
    price_usd = models.DecimalField(max_digits=40, decimal_places=30,default=0)
    capitalization = models.DecimalField(max_digits=22, decimal_places=2,default=0)
    market_supply = models.DecimalField(max_digits=22, decimal_places=2,default=0)
    total_supply = models.DecimalField(max_digits=22, decimal_places=2,default=0)
    price_updated = models.DateTimeField(blank=True, null=True)
    last_update_try = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    def __str__(self):
        return self.name

    def update_price(self,data = None):
        if self.id not in [0,5]:
            if data is None:
                data = Coin_Data_Api_Call(self.coinmarketcap_com_id)
                print("Data Fetched...")

            self.price_btc = (data['price_btc']) or 0
            self.price_usd = data['price_usd'] or 0
            self.capitalization = data['market_cap_usd'] or 0
            self.market_supply = data['available_supply'] or 0
            self.total_supply = data['total_supply'] or 0
            if data['last_updated']:
                self.price_updated = datetime.datetime.fromtimestamp(float(data['last_updated']), tz=timezone.get_current_timezone()) # timezone.get_current_timezone()
            self.last_update_try = timezone.now()
            self.save()

class CoinPortfolio(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    cost_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    #entries
    balance_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    balance_euros = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    profit = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    profit_percent = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    class Meta:
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'

    def __str__(self):
        return self.name

    def update_total(self):
        summ = 0;
        for ent in self.entries.all():
            ent.update_balance()
            summ = summ + ent.balance_usd
        self.balance_usd = summ
        self.balance_euros = float(summ)/1.11
        self.profit = summ - float(self.cost_usd)
        self.profit_percent = 100 * (float(self.profit))  / float(self.cost_usd)

        self.save()

#from CoinTradeMarket.models import Balance

class Balance(models.Model):
    name = models.CharField(max_length=200)
    coin = models.ForeignKey(Coin)
    balance = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    balance_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    #balance_euros = models.DecimalField(max_digits=40, decimal_places=10,default=0)


    def __str__(self):
        return (self.name)

    # def update_prices(self):
    #     self.coin.update_prices()
    #     self.balance_usd = float(self.balance) * float(self.coin.price_usd)
    #     self.save()

class CoinPortfolioEntry(Balance):
    portfolio = models.ForeignKey(CoinPortfolio, related_name='entries')
    public_address = models.CharField('Public Key', max_length = 150)
    #coin = models.ForeignKey(Coin)
    #balance = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    buy_price_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    #balance_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    ##balance_euros = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    profit = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    profit_percent = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    class Meta:
        verbose_name = 'Portfolio Entry'
        verbose_name_plural = 'Portfolio Entries'

    def __str__(self):
        return (self.portfolio.name + "_" +self.coin.name)

    def update_balance(self):
        self.coin.update_price()
        self.balance_usd = float(self.balance) * float(self.coin.price_usd)
        if self.buy_price_usd == 0:
            self.profit = 0
            self.profit_percent = 0
        else:
            self.profit = (float(self.coin.price_usd) - float(self.buy_price_usd)) * float(self.balance)
            self.profit_percent = 100 * (float(self.coin.price_usd) - float(self.buy_price_usd)) / float(self.buy_price_usd)

        self.save()

# To Do
    # def check_balance(self):
    #     self.save()
    # def send_Transaction(self):
    #     self.save()
    # def verify_Transaction(self):
    #     self.save()
