import csv
import datetime 

class Coat:
  def __init__(self,id):
    self.id = id
    self.received = [] 
    self.dispatched = []
    self.status = ''
    
  def getstatus(self):
  	r = len(self.received)
  	d = len(self.dispatched)
  	if r > 0 and d > 0:
  		a = self.received[-1]
  		b = self.dispatched[-1]
  		delta = a - b
  		if delta.days < 0:
  			return 'out'
  		else:
  			return 'in'
  	elif r > 0:
  		return 'in'
  	else:
  		return 'out'
  	
  def history(self):
  	r = 0
  	lenr = len(self.received)
  	d = 0
  	lend = len(self.dispatched)
  	tl = lenr + lend
  	for i in range(tl):
  		isreceived = 0
  		s = ''
  		#s += str(r) + ' ' + str(d) + ' ' + str(tl)
  		#s = s.ljust(8)
  		s += self.id.ljust(10)
  		if r < lenr and d < lend:
  			delta = self.received[r] - self.dispatched[d]
  			if delta.days <= 0:
  				isreceived = 1
  			else:
  				isreceived = 0
  		elif r < lenr:
  			isreceived = 1
  		#print(isreceived)
  		if isreceived:
  			s += str(self.received[r])
  			r += 1
  		else:
  			s += ''.ljust(12)
  			s += str(self.dispatched[d])
  			d += 1
  		print(s)


class Owner:
  def __init__(self,id,name):
    self.id = id
    self.name = name
    self.coat = []

  def check(self,s):
    for c in self.coat:
      if c.id == s:
        return True
    return False


def dayoffset(o):
	#returns difference between 
	#today and given date
	a = datetime.date.today()
	b = datetime.timedelta(days = o)
	return a - b


def buildtree():
	owner = []
	#bulid data structure from files
	with open('mainui/employees.csv', 'r' ) as file:
	  reader = csv.reader(file)
	  for row in reader:
	    if row[1] != '':
	      owner.append(Owner(row[0],row[1]))
	      
	with open('mainui/coats.csv', 'r' ) as file:
	  reader = csv.reader(file)
	  for row in reader:
	    if row == '':
	    	pass
	    	#break
	    c = Coat(row[0])
	    f = False
	    for o in owner:
	    	if o.id == row[1]:
	    		f = True
	    		o.coat.append(c)
	    		break
	    if not f:
	      owner[0].coat.append(c)
	      
	with open('mainui/received.csv', 'r' ) as file:
	  reader = csv.reader(file)
	  for row in reader:
	    a = datetime.datetime.strptime(row[1],'%d/%m/%Y').date()
	    c = [c for o in owner for c in o.coat if c.id == row[0]]
	    if len(c) == 0:
	    	owner[0].coat.append(Coat(row[0]))
	    [c.received.append(a) for o in owner for c in o.coat if c.id == row[0]]

	with open('mainui/dispatched.csv', 'r' ) as file:
	  reader = csv.reader(file)
	  for row in reader:
	    a = datetime.datetime.strptime(row[1],'%d/%m/%Y').date()
	    [c.dispatched.append(a) for o in owner for c in o.coat if c.id == row[0]]

	#sort dates
	for o in owner:
	  for c in o.coat:
	    c.received = sorted(c.received)
	    c.dispatched = sorted(c.dispatched)
	    c.status = c.getstatus()
	return owner
	
	
def displaytree(owner):
	#print data structure and highlight
	#and missing coats and coats received
	#this week
	t = datetime.date.today()
	for o in owner:
	  print('{0}: {1} ({2} coats)'.format(o.id,o.name,len(o.coat)))
	  if len(o.coat) >0:
	  	print("\n   coat        last seen")
	  	for c in o.coat:
	  	  scanlist = c.received + c.dispatched
	  	  scanlist = sorted(scanlist)
	  	  lastscanned = str(scanlist[-1]) + ' ' + c.status
	  	  if scanlist[-1] < dayoffset(60):
	  	  	lastscanned += ' and missing'
	  	  print('   ' + c.id + '    ' + lastscanned)
	  print('\n\n')
	  
	  
def parse(s,owner):
	#parse user input 
	tc = []
	s = s.lower()
	if ' ' in s:
		c,t = s.split(' ',1)
		
		if c == 'n':#name search
			result = [o for o in owner if t in o.name.lower()]
			if len(result) == 0: 
			  print('Not Found')
			i = 0
			for r in result:
			  print()
			  print(r.name)
			  for oc in r.coat:
			  	i += 1
			  	tc.append(oc.id)
			  	if len(oc.received) != 0 or len(oc.dispatched) != 0:
			  		print(str(i) + ':' + oc.id + ' - ' + str(oc.status))
			nc = 0
			while nc != 'q':
				nc = input('\n'.strip())
				if nc == 'q': break
				if nc[0] in ['n','c','d','r']:
					parse(nc,owner)
				
				elif int(nc) > 0 and int(nc) <= len(tc):
					parse('c ' + tc[int(nc)-1],owner)
				else:
					print('not found\npick 1 - ' + str(len(tc)))
				
		elif c == 'c':#coat search
			lastowner = ''
			for o in owner:
				for oc in o.coat:
					if t in oc.id:
						if not lastowner == o.name:
							print()
							print(o.name)
							lastowner = o.name
							s = ''
							#s += 'debug'.ljust(8)
							s += 'coat'.ljust(10)
							s += 'received'.ljust(12)
							s += 'dispatched'
							print(s)
						oc.history()
		elif c == 'd':#date search
			pass
	else:
		if s == 'r':#reset
		  owner = buildtree()
		  displaytree(owner)


if __name__ == '__main__':
	owner = buildtree()
	displaytree(owner)
	while True:
		parse(input('\n').strip(),owner)