import SocketServer

from sbd import MobileOriginatedMessage


class IridiumTcpHandler(SocketServer.StreamRequestHandler):

    def finish(self):
        print MobileOriginatedMessage.parse(self.rfile).data
