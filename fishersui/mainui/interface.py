import csv
import datetime 

class Transaction:
	def __init__(self,date,type):
		self.date = date
		self.type = type
		self.week = date.strftime('%V')

	def __lt__(self,other):
		return self.date < other.date


class Coat:
	def __init__(self,id):
		self.id = id
		self.transaction = []
		self.status = ''
		self.history = ''

	def getstatus(self,offset=14):
		try:
			if self.transaction[-1].type == 1:
				return 'in'
			elif self.transaction[-1].type == 0 and self.transaction[-1].date < dayoffset(offset):
				return 'missing'
			else:
				return 'out'
		except:
			return 'unknown'
		
	def gethistory(self):
		if len(self.transaction) == 0:
			s = ''
		else:
			s = '<table><thead><tr><th>Received</th><th>Dispatched</th><th>Week</th></tr></thead>\n'
			for t in self.transaction:
				if t.type == 1:
					s += '<tr><td>' + str(t.date) + '</td><td></td><td>'+str(t.week)+'</td></tr>\n'
				else:
					s += '<tr><td/><td>' + str(t.date) + '</td><td>'+str(t.week)+'</td></tr>\n'
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
				[c.transaction.append(Transaction(a,1)) for o in owner for c in o.coat if c.id == row[0]]

	with open('mainui/dispatched.csv', 'r' ) as file:
		reader = csv.reader(file)
		for row in reader:
			a = datetime.datetime.strptime(row[1],'%d/%m/%Y').date()
			if a > dayoffset(historylen):
				c = [c for o in owner for c in o.coat if c.id == row[0]]
				if len(c) == 0:
					owner[0].coat.append(Coat(row[0]))
				[c.transaction.append(Transaction(a,0)) for o in owner for c in o.coat if c.id == row[0]]

	#cleanup
	for o in owner:
		for c in o.coat:
			c.transaction = sorted(c.transaction)
			c.status = c.getstatus()
			c.history = c.gethistory()
	return owner