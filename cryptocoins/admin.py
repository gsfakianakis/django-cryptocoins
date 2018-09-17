from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


# Register your models here.
from .models import *


def update_price(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_price()
update_price.short_description = "Update Price"


class CoinAdmin(admin.ModelAdmin):
    #list_display = ('id', 'name', 'price_btc')
    list_display = [field.name for field in Coin._meta.fields]
    ordering = ('id',)
    actions = [update_price]

admin.site.register(Coin,CoinAdmin)

def update_totals(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_total()
update_totals.short_description = "Update Totals"

def reprocess_transactions(modeladmin, request, queryset):
    for obj in queryset:
        obj.ReProcessTransactions()
reprocess_transactions.short_description = "ReProcess Transactions"


class CoinPortfolioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CoinPortfolio._meta.fields]
    ordering = ('id',)
    actions = [update_totals,reprocess_transactions]
    readonly_fields = ['invested_usd','cash_outs_usd','balance_usd','balance_euros','profit','profit_percent'] #

admin.site.register(CoinPortfolio,CoinPortfolioAdmin)

##

def update_balance_entry(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_balance()
update_balance_entry.short_description = "Update Prices Portfolio Entry"

class CoinPortfolioEntryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CoinPortfolioEntry._meta.fields]
    ordering = ('id',)
    actions = [update_balance_entry]
    readonly_fields = ['buy_price_usd','profit','profit_percent','balance_usd']
    list_filter = (
        # for ordinary fields
        # ('a_charfield', DropdownFilter),
        # for related fields
        ('portfolio', RelatedDropdownFilter),
        ('coin', RelatedDropdownFilter),

    )


admin.site.register(CoinPortfolioEntry,CoinPortfolioEntryAdmin)

##

class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.fields]
    ordering = ('id',)
    actions = []
    readonly_fields = ['balance_usd','balance','diff_balance']


admin.site.register(Address,AddressAdmin)
##

def process_transaction(modeladmin, request, queryset):
    for obj in queryset:
        obj.process()
process_transaction.short_description = "Process"

class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields]
    readonly_fields = ['processed'] # ,'amount_usd_DoT'
    ordering = ('id',)
    actions = [process_transaction]
    list_filter = (
        # for ordinary fields
        ('type_tr', ChoiceDropdownFilter),
        # for related fields
        ('portfolio', RelatedDropdownFilter),
        # ('type_tr', RelatedDropdownFilter),


    )


admin.site.register(Transaction,TransactionAdmin)
