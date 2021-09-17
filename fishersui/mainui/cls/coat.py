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