import SocketServer

from sbd import MobileOriginatedMessage


class IridiumTcpHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        print MobileOriginatedMessage.parse(self.rfile).data
