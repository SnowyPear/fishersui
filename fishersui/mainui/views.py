from django.shortcuts import render
from django.http import HttpResponse
from . import interface
import datetime


historylen = 600
# Create your views here.

def index(request):
    owner = interface.buildtree(historylen)
    
    remove = [c for o in owner for c in o.coat if len(c.transaction) == 0]

    for r in remove:
        [o.coat.remove(c) for o in owner for c in o.coat if c.id == r.id]

    result = [o for o in owner if len(o.coat) > 0]

    context = {
        'page_title': 'Fishers Coats', 
  	    'owner': result,
        'color' : '#359C37' 
    }
    return render(request, 'fishers/owners.html', context)

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
    return render(request, 'fishers/status.html', context)

def search(request,term=''):
    owner = interface.buildtree(historylen)
    
    #remove = [c for o in owner for c in o.coat if term.lower not in str(o.name).lower]

    #for r in remove:
    #    [o.coat.remove(c) for o in owner for c in o.coat if c.id == r.id]
    def lower(a):
        return str(a).lower()

    result = [o for o in owner if term.lower() in o.name.lower()]

    context = {
        'page_title': 'Fishers Laundry - ' + term, 
  	    'owner': result,
        'color' : '#359C37' 
    }
    return render(request, 'fishers/owners.html', context)

def deliveries(request,week=''):
    owner = interface.buildtree(historylen)
    deliveries = []

    thisweek = datetime.date.today()
    thisweek = int(thisweek.strftime('%V'))

    if week == 'last':
        listmax = 1
    else:
        try:
            if int(week) > 0:
                listmax = 1
                thisweek = int(week)
        except:
            listmax = 20


    for r in range(listmax):
        d = []
        for o in owner:
            for c in o.coat:
                for t in c.transaction:
                    if int(t.week) == thisweek-r:
                        if t.type:
                            type = 'received'
                        else:
                            type = 'dispatched'
                        if int(t.week) == thisweek:
                            style = "max-height: 9999px;"
                        else:
                            style = "max-height: null;"
                        d.append([t.week,c.id,c.status,o.name,type,t.date.strftime('%d %B \'%y'),style])
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
    return render(request, 'fishers/deliveries.html', context)