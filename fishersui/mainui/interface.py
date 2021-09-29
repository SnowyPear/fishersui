import csv
import datetime 

class Coat:
	def __init__(self,id):
		self.id = id
		self.received = [] 
		self.dispatched = []
		self.status = ''
		self.history = ''
	
	
	def getstatus(self,offset = 14):
		r = len(self.received)
		d = len(self.dispatched)
		if r > 0 and d > 0:
			a = self.received[-1]
			b = self.dispatched[-1]
			delta = a - b
			if delta.days < 0:
				if self.dispatched[-1] < dayoffset(offset):
					return 'missing'
				else:
					return 'out'
			else:
				return 'in'
		elif r > 0:
			return 'in'
		elif d > 0:
			if self.dispatched[-1] < dayoffset(offset):
				return 'missing'
			else:
				return 'out'
		else:
			return 'unknown'
		
	def gethistory(self):
		r = 0
		lenr = len(self.received)
		d = 0
		lend = len(self.dispatched)
		tl = lenr + lend
		if tl == 0:
			s = ''
		else:
			s = '<table><tr><th>Received</th><th>Dispatched</th></tr>\n'
			for i in range(tl):
					isreceived = 0
					if r < lenr and d < lend:
						delta = self.received[r] - self.dispatched[d]
						if delta.days <= 0:
							isreceived = 1
						else:
							isreceived = 0
					elif r < lenr:
						isreceived = 1
					if isreceived:
						s += '<tr><td>' + str(self.received[r]) + '</td><td></td></tr>\n'
						r += 1
					else:
						s += '<tr><td/><td>' + str(self.dispatched[d]) + '</td></tr>\n'
						d += 1
			s += '</table>'
		return s


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


def buildtree(historylen):
	owner = []
	coatlist = []
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
			if a > dayoffset(historylen):
				c = [c for o in owner for c in o.coat if c.id == row[0]]
				if len(c) == 0:
					owner[0].coat.append(Coat(row[0]))
				[c.received.append(a) for o in owner for c in o.coat if c.id == row[0]]

	with open('mainui/dispatched.csv', 'r' ) as file:
		reader = csv.reader(file)
		for row in reader:
			a = datetime.datetime.strptime(row[1],'%d/%m/%Y').date()
			if a > dayoffset(historylen):
				c = [c for o in owner for c in o.coat if c.id == row[0]]
				if len(c) == 0:
					owner[0].coat.append(Coat(row[0]))
				[c.dispatched.append(a) for o in owner for c in o.coat if c.id == row[0]]

	#cleanup
	for o in owner:
		for c in o.coat:
			c.received = sorted(c.received)
			c.dispatched = sorted(c.dispatched)
			c.status = c.getstatus()
			c.history = c.gethistory()

	return owner