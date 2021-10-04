from django.shortcuts import render
from django.http import HttpResponse
from . import interface
import datetime


historylen = 60
# Create your views here.

def index(request):
    owner = interface.buildtree(historylen)
    
    remove = [c for o in owner for c in o.coat if len(c.transaction) == 0]

    for r in remove:
        [o.coat.remove(c) for o in owner for c in o.coat if c.id == r.id]

    result = [o for o in owner if len(o.coat) > 0]

    context = {
        'page_title': 'Fishers Laundry', 
  	    'owner': result,
        'color' : '#359C37' 
    }
    return render(request, 'owners/owners.html', context)

def reports(request,status='missing',historylen=historylen):
    if status == 'unknown':
        historylen = 9999

    owner = interface.buildtree(int(historylen))

    for o in owner:
        o.coat = [c for c in o.coat if c.status == status]

    result = [o for o in owner if len(o.coat) > 0]

    context = {
        'page_title': 'Fishers Laundry', 
        'owner': result,
        'status': status,
        'color' : '#359C37' 
    }
    return render(request, 'reports/status.html', context)

def search(request,term=''):
    owner = interface.buildtree(historylen)
    
    remove = [c for o in owner for c in o.coat if len(c.transaction) == 0]

    for r in remove:
        [o.coat.remove(c) for o in owner for c in o.coat if c.id == r.id]

    result = [o for o in owner if len(o.coat) > 0]

    context = {
        'page_title': 'Fishers Laundry', 
  	    'owner': result,
        'color' : '#359C37' 
    }
    return render(request, 'owners/owners.html', context)

def deliveries(request,week=''):
    owner = interface.buildtree(historylen)
    deliveries = []
    week = datetime.date.today()
    week = int(week.strftime('%V'))

    for r in range(10):
        d = []
        for o in owner:
            for c in o.coat:
                for t in c.transaction:
                    if int(t.week) == week-r:
                        if t.type:
                            type = 'received'
                        else:
                            type = 'dispatched'
                        d.append([t.week,c.id,c.status,o.name,type,t.date.strftime('%d %B \'%y')])
                        d =  sorted(d, key=lambda x: x[4], reverse=True)
        if not d == []:
            deliveries.append(d)

    result = [o for o in owner if len(o.coat) > 0]

    context = {
        'page_title': 'Fishers Laundry', 
  	    'owner': result,
        'deliveries': deliveries,
        'color' : '#359C37' 
    }
    return render(request, 'deliveries/deliveries.html', context)