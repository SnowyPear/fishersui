from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import interface
import datetime


historylen = 9999
# Create your views here.

def index(request):
    #return redirect('/deliveries?coat=30371795')
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
    
    result = [] 

    def lower(a):
        return str(a).lower()
    for o in owner:
        match = 0
        currentowner = interface.Owner(o.id,o.name)
        if term.lower() in o.name.lower():
             match = 1
             currentowner = o
        for c in o.coat:
            if term in c.id:
                currentowner.coat.append(c)
                match = 1
        if match == 1:
            result.append(currentowner)

    context = {
        'page_title': 'Fishers Laundry - ' + term, 
  	    'owner': result,
        'color' : '#359C37' 
    }
    return render(request, 'fishers/owners.html', context)

def deliveries(request,week=''):
    owner = interface.buildtree(historylen)
    deliveries = []
    highlightedcoat = request.GET.get('coat','')
    extend = request.GET.get('extend','')

    thisweek = datetime.date.today()
    thisweek = int(thisweek.strftime('%V'))

    for r in range(52):
        d = list() 
        extend=False
        style = "max-height: 0px;"
        for o in owner:
            for c in o.coat:
                for t in c.transaction:
                    if int(t.week) == thisweek-r:
                        if t.type:
                            type = 'received'
                        else:
                            type = 'dispatched'
                        #expand the first card
                        if len(deliveries) < 1 and highlightedcoat == '' :
                            style = "max-height: 9999px;"
                        if c.id == highlightedcoat:
                            highlight = 'background-color:#406A6A;'
                            style = "max-height: 9999px;"
                            extend=True
                            print(highlightedcoat)
                            print(c.id)
                        else:
                            highlight = ''
                        d.append([t.week,c.id,c.status,o.name,type,t.date.strftime('%d %B \'%y'),style,highlight])
                        d =  sorted(d, key=lambda x: x[4], reverse=True)
                        
        try:
            if not d[-1] == []:
                print(d)
                deliveries.append(d)
        except:
        	pass
        	#print("error") 
            
        if extend == True:
        	d[0][6]= "max-height: 9999px;"
        
    result = ""# [o for o in owner if len(o.coat) > 0]
            
    context = {
        'page_title': 'Fishers Laundry', 
  	   'owner': result,
        'deliveries': deliveries,
        'color' : '#359C37' 
    }
    return render(request, 'fishers/deliveries.html', context)


def svg(request):
    return render(request, 'fishers/svg.html')
