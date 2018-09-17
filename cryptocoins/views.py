from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.core.management import call_command
from django.http import HttpResponse
from io import StringIO
from .models import *



def Update_Coins(request):
    out = StringIO()
    call_command('J1_Update_Coins', stdout=out)
    return HttpResponse(str(out.getvalue())+ "\n Coins Updated")


def ReProcess_Portfolio(request,pk):
    pfolio = get_object_or_404(CoinPortfolio, id=pk)
    pfolio.ReProcessTransactions()
    return HttpResponse("Portfolio Reprocessed")
