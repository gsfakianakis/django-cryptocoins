from django.shortcuts import render
# Create your views here.
from django.core.management import call_command
from django.http import HttpResponse
from io import StringIO



def Update_Coins(request):
    out = StringIO()
    call_command('J1_Update_Coins', stdout=out)
    return HttpResponse(str(out.getvalue())+ "\n Coins Updated")
