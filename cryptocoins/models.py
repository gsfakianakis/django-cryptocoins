from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
import datetime
from .functions_nomodels import Coin_Data_Api_Call, Get_USD_Euro_Rate

from django.contrib.auth.models import User
#from cryptocoins.signals import *

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
    price_updated = models.DateTimeField(blank=True, null=True, default = (timezone.now() - timezone.timedelta(days=1))) # Something random - days=1
    last_update_try = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    def __str__(self):
        return self.name

    def update_price(self,data = None):
        print("================================")
        print("     " + self.name)
        if self.id not in [-1,0]:
            Valid_Update_Time = (datetime.datetime.now(tz=timezone.UTC()) -  self.price_updated) > datetime.timedelta(minutes=5)
            #print(datetime.datetime.now(tz=timezone.UTC()))
            #print(self.price_updated)
            Data_Available = data is not None
            if not(Data_Available) and Valid_Update_Time:
                data = Coin_Data_Api_Call(self.coinmarketcap_com_id)
                print("Data Fetched for " + str(self.name))
                Data_Available = 1
                if data is None:
                    Data_Available = 0


            if Data_Available:
                self.price_btc = (data['price_btc']) or 0
                self.price_usd = data['price_usd'] or 0
                self.capitalization = data['market_cap_usd'] or 0
                self.market_supply = data['available_supply'] or 0
                self.total_supply = data['total_supply'] or 0
                if data['last_updated']:
                    self.price_updated = datetime.datetime.fromtimestamp(float(data['last_updated']), tz=timezone.get_current_timezone()) # timezone.get_current_timezone()
        elif self.id in [-1]:
            Day_Today = datetime.datetime.today().weekday()
            Valid_Day = Day_Today not in [5,6]
            Valid_Update_Time = (datetime.datetime.now(tz=timezone.UTC()) -  self.price_updated) > datetime.timedelta(hours=24)

            if Valid_Update_Time and Valid_Day:
                price, date = Get_USD_Euro_Rate()
                self.price_usd = price
                self.price_updated = date
                print("Data Fetched for " + str(self.name))

        elif self.id in [0]:
            pass
            #print("Hi I am US Dollar.")
        else:
            pass

        self.last_update_try = timezone.now()
        self.save()

class Address(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    coin = models.ForeignKey(Coin)
    balance = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    balance_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    diff_balance = models.DecimalField(max_digits=40, decimal_places=10,default=0) # difference from Entries
    public_address = models.CharField('Public Key', max_length = 150)


    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.name

    def update_price(self,data = None):
            self.save()
    def update_balance(self,data = None):
            self.save()
    def update_balance_diff(self,data = None):
            self.save()



class CoinPortfolio(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    invested_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0) #costs
    cash_outs_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0) #ccash outs
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
        euro = Coin.objects.get(id = -1)
        euro.update_price()
        self.balance_euros = float(summ)/float(euro.price_usd)
        self.profit = summ + float(self.cash_outs_usd) - float(self.invested_usd)
        if (self.invested_usd > 0):
            self.profit_percent = 100 * (float(self.profit))  / float(self.invested_usd)

        self.save()

    def ReProcessTransactions(self):
        self.invested_usd = 0
        self.cash_outs_usd = 0
        self.balance_usd = 0
        self.balance_euros = 0
        self.profit = 0
        self.profit_percent = 0

        trs = self.transactions.all()
        entrs = self.entries.all()
        for ent in entrs:
            ent.balance = 0
            ent.balance_usd = 0
            ent.buy_price_usd = 0
            ent.profit = 0
            ent.profit_percent = 0
            ent.save()

        print("######################### Re Processing #####################")

        for tr in trs:
            print(50*"/")
            print(tr.description)
            tr.processed = 0
            tr.save()
            tr.process(Part_of_ReProcess = 1)
        self.update_total()

@receiver(signals.post_save, sender=CoinPortfolio)
def create_portfolio_default_entries(sender, instance, created, **kwargs):
    if created:
        CoinPortfolioEntry.objects.create(portfolio=instance, coin_id = -1, name=(instance.name + " " + 'Euro')) #Euro
        CoinPortfolioEntry.objects.create(portfolio=instance, coin_id = 0, name=(instance.name + " " + 'US Dollar')) #USD
        CoinPortfolioEntry.objects.create(portfolio=instance, coin_id = 1, name=(instance.name + " " + 'BTC'))
        CoinPortfolioEntry.objects.create(portfolio=instance, coin_id = 2, name=(instance.name + " " + 'ETH'))
        CoinPortfolioEntry.objects.create(portfolio=instance, coin_id = 17, name=(instance.name + " " + 'ZEN')) # Add more below.


class Balance(models.Model):
    name = models.CharField(max_length=200)
    coin = models.ForeignKey(Coin)
    balance = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    balance_usd = models.DecimalField('Balance in USD',max_digits=40, decimal_places=10,default=0)


    def __str__(self):
        return (self.name)

class CoinPortfolioEntry(Balance):
    portfolio = models.ForeignKey(CoinPortfolio, related_name='entries')
    address = models.ForeignKey(Address, related_name='entries',null=True,default=None)

    buy_price_usd = models.DecimalField(max_digits=40, decimal_places=10,default=0)
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


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
    (1, 'Input'),
    (2, 'Output'),
    (3, 'Payment/Income'),
    (4, 'Cost/Expenses'),
    (5, 'Exchange Sell'),
    (6, 'Exchange Buy'),
    )

    portfolio = models.ForeignKey(CoinPortfolio, related_name='transactions')
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField('Description', max_length = 1500)
    type_tr = models.IntegerField('Type',choices=TRANSACTION_TYPE_CHOICES)


    amount = models.DecimalField(max_digits=40, decimal_places=10,default=0)
    entry = models.ForeignKey(CoinPortfolioEntry,blank=True, null=True,default=None)
    amount_usd_DoT = models.DecimalField('Amount USD DoT',max_digits=40, decimal_places=10,blank=True, null=True,default=-1)

    processed = models.IntegerField('Processed',default = 0)


    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return ( str(self.date) + "_" + (self.description) + "_" + self.portfolio.name + "_" + self.entry.coin.name)

    def process(self,reverse = 0,Part_of_ReProcess = 0):
        entry = self.entry

        if self.processed == 0:
            print('Unprocessed')
            if self.type_tr == 1:
                entry.balance = entry.balance + self.amount
                entry.update_balance() # Price of coin is updated here
                if entry.coin.id not in [-1]:
                    self.portfolio.invested_usd +=  self.amount * entry.coin.price_usd
                    coin_price_DoT = entry.coin.price_usd
                else:
                    euro_price_usd_in_date, date = Get_USD_Euro_Rate(self.date)
                    #print(euro_price_usd_in_date)
                    self.portfolio.invested_usd +=  self.amount * (euro_price_usd_in_date)
                    coin_price_DoT = euro_price_usd_in_date

                self.portfolio.save()

            elif self.type_tr == 2:
                entry.balance = entry.balance - self.amount
                entry.update_balance() # Price of coin is updated here
                #self.portfolio.cash_outs_usd +=  self.amount * entry.coin.price_usd
                if entry.coin.id not in [-1]:
                    self.portfolio.cash_outs_usd +=  self.amount * entry.coin.price_usd
                    coin_price_DoT = entry.coin.price_usd
                else:
                    euro_price_usd_in_date, date = Get_USD_Euro_Rate(self.date)
                    #print(euro_price_usd_in_date)
                    self.portfolio.cash_outs_usd +=  self.amount * euro_price_usd_in_date
                    coin_price_DoT = euro_price_usd_in_date
                self.portfolio.save()

            elif self.type_tr == 3:
                entry.balance = entry.balance + self.amount
                entry.update_balance() # Price of coin is updated here
                coin_price_DoT = entry.coin.price_usd

            elif self.type_tr == 4:
                entry.balance = entry.balance - self.amount
                entry.update_balance() # Price of coin is updated here
                coin_price_DoT = entry.coin.price_usd

            elif self.type_tr == 5:
                entry.balance = entry.balance - self.amount
                entry.update_balance() # Price of coin is updated here
                coin_price_DoT = entry.coin.price_usd

            elif self.type_tr == 6:
                entry.balance = entry.balance + self.amount
                entry.update_balance() # Price of coin is updated here
                coin_price_DoT = entry.coin.price_usd

            else:
                print('Unknown Type.')

            print("Type Specific calculations finished")
            entry.save()
            if not Part_of_ReProcess:
                self.portfolio.update_total()
            self.processed = 1
            if self.amount_usd_DoT is None or (self.amount_usd_DoT == -1):
                self.amount_usd_DoT = float(self.amount) * float(coin_price_DoT)
            self.save()

@receiver(signals.post_save, sender=Transaction)
def process_transaction(sender, instance, created, **kwargs):
    if created:
        instance.process()
