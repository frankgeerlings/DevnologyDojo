import SimpleHTTPServer, SocketServer
import urlparse, os
from pprint import pprint
from StringIO import StringIO
import re
from math import sqrt

PORT = 3000

def F(n):
	return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

class FibonacciHandler():
	def handle(self, group):
		print 'FIBO %s' % group[0]
		nummer = int(group[0])
		result = '%d' % F(nummer - 1)
		print result
		return result

class MinusHandler():
	def handle(self, group):
		print 'MINUS %s - %s' % (group)
		a, b = map(int, group)
		return "%d" % (a - b)

class SommetjesHandler():
	def handle(self, group):
		print 'A+B*C %s - %s' % (group)
		a, b, c = map(int, group)
		return "%d" % (a + b * c)

class PowerHandler():
	def handle(self, group):
		print 'POWER %s ^ %s' % (group)
		a, b = map(int, group)
		return "%d" % (a ^ b)

straightAnswers = {
	'who is the Prime Minister of Great Britain': 'Cameron',
	'what currency did Spain use before the Euro': 'Peseta',
	'what colour is a banana': 'yellow'
}

regexable = {
	'what is the (.*?)(nd|th|st) number in the Fibonacci sequence': FibonacciHandler(),
	'what is (.*?) minus (.*?)': MinusHandler(),
	'what is (.*?) plus (.*?) multiplied by (.*?)': SommetjesHandler(),
	'what is (.*?) to the power of (.*?)': PowerHandler()
}

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):

       # Parse query data to find out what was requested
       parsedParams = urlparse.urlparse(self.path)

       q = parsedParams.query

       vraag = q.replace('%20', ' ').split(':', 1)[1][1:]

       f = StringIO()
       f.write('Frank')

       length = f.tell()
       f.seek(0)
       self.send_response(200)
       self.send_header("Content-type", "text/html")

       self.end_headers()

       if (straightAnswers.has_key(vraag)):
       		antwoord = straightAnswers[vraag]
       		print antwoord
       		self.wfile.write(antwoord);
       		print 'BEANTWOORD'
       		return

       for i in regexable.keys():
       		s = re.search(i, vraag)

       		if (s is not None):
       			pprint(s.groups())
       			self.wfile.write(regexable[i].handle(s.groups()))

       self.wfile.write('%d' % length)

       return

Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()