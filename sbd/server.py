import SocketServer


class IridiumTCPHandler(SocketServer.BaseRequestHandler):

    def finish(self):
        print self.rfile.read()
