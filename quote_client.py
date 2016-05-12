#!/Users/kawasakitaku/Documents/python-PVM/ln-python3.4/bin/python2.7

from twisted.internet import protocol,reactor

class QuoteProtocol(protocol.Protocol):
    def __init__(self,factory):
        self.factory = factory
        
    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        self.transport.write(self.factory.quote)
        
    def dataReceived(self,data):
        print("Received data" ,data)
        self.transport.loseConnection()

class QuoteClientFactory(protocol.ClientFactory):
    def __init__(self,quote):
        self.quote = quote

    def buildProtocol(self,addr):
        return QuoteProtocol(self)

    def clientConnectionFailed (self,connector,reason):
        print("Connection Failed:" ,reason.getErrorMessage())
        maybeStopReactor()

    def clientConnectionLost(self,connector,reason):
        print("Connection Lost:" ,reason.getErrorMessage())
        maybeStopReactor()

def maybeStopReactor():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()


quotes = [
    "You snooze you lose",\
    "The early birds gets worm",\
    "Carp diem"\
    ]

quote_counter = len(quotes)

for quote in quotes:
    reactor.connectTCP('localhost',8000, QuoteClientFactory(quote))
reactor.run()        
        
    
