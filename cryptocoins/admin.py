from django.contrib import admin

# Register your models here.
from .models import *


def update_prices(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_prices()
update_prices.short_description = "Update Price"


class CoinAdmin(admin.ModelAdmin):
    #list_display = ('id', 'name', 'price_btc')
    list_display = [field.name for field in Coin._meta.fields]
    ordering = ('id',)
    actions = [update_prices]

admin.site.register(Coin,CoinAdmin)

def update_totals(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_total()
update_totals.short_description = "Update Totals"

class CoinPortfolioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CoinPortfolio._meta.fields]
    ordering = ('id',)
    actions = [update_totals]

admin.site.register(CoinPortfolio,CoinPortfolioAdmin)

##

def update_prices_entry(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_prices()
update_prices_entry.short_description = "Update Prices Portfolio Entry"

class CoinPortfolioEntryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CoinPortfolioEntry._meta.fields]
    ordering = ('id',)
    actions = [update_prices_entry]


admin.site.register(CoinPortfolioEntry,CoinPortfolioEntryAdmin)
