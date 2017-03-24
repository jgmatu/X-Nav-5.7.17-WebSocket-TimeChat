#!/usr/bin/python
# Example WebSocket Server interface
# Original taken from: https://github.com/opiate/SimpleWebSocketServer
# Under the MIT license

import signal
import sys
import ssl
import logging
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class SimpleEcho(WebSocket):

    def handleMessage(self):
        if self.data is None:
            self.data = ''

        if self.isTime():
            self.sendTime()
            return

        print "Echo Received : " + self.data

        try:
            self.sendMessage(str(self.data))
            print "Echo Send : " + self.data
        except Exception as n:
            print n

    def handleConnected(self):
        print "Echo Connected : " + self.address

    def handleClose(self):
        print "Echo Closed : " + self.address


class SimpleChat(WebSocket):

    def handleMessage(self):
        if self.data is None:
            self.data = ''

        if self.isTime():
            self.sendTime()
            return

        print "Chat Received : " + self.data

        for client in self.server.connections.itervalues():
            if client != self:
                try:
                    client.sendMessage("Node [" + str(self.address[0]) + ":" + str(self.address[1]) + "]" " Message : " + str(self.data))
                    print "Chat Send : " + self.data + " address : " + str(self.address)
                except Exception as n:
                    print n

    def handleConnected(self):
        print "Chat Connected : " + self.address

        for client in self.server.connections.itervalues():
            if client != self:
                try:
                    client.sendMessage(str(self.address[0]) + ' - connected')
                    print "Send : Connected"
                except Exception as n:
                    print n

    def handleClose(self):
        print "Chat Closed : " + self.address

        for client in self.server.connections.itervalues():
            if client != self:
                try:
                    client.sendMessage(str(self.address[0]) + ' - disconnected')
                    print "Send : Disconnected"
                except Exception as n:
                    print n

if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
    parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

    (options, args) = parser.parse_args()

    cls = SimpleEcho
    if options.example == 'chat':
        cls = SimpleChat

    if options.ssl == 1:
        server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
    else:
        server = SimpleWebSocketServer(options.host, options.port, cls)

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    server.serveforever()
