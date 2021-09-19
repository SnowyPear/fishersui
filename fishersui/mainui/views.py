from django.shortcuts import render
from django.http import HttpResponse
from . import interface

# Create your views here.

def index(request):
    owner = interface.buildtree()

    context = {
        "page_title": "Fishers Laundry", 
  	    "owner": owner,
        "color" : "#359C37" 
    }
    return render(request, 'owners/owners.html', context)

def missingreport(request,status="missing"):
    owner = interface.buildtree()
    result = [o for o in owner for c in o.coat if c.status==status]

    context = {
        "page_title": "Fishers Laundry", 
        "owner": result,
        "status": status,
        "color" : "#359C37" 
    }
    return render(request, 'reports/status.html', context)
