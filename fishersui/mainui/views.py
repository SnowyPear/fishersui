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

def missingreport(request):
    owner = interface.buildtree()
    context = {
    "page_title": "Fishers Laundry", 
  	"owner": owner,
   "color" : "#359C37" 
    }
    return render(request, 'reports/missing.html', context)