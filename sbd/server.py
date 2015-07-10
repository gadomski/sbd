import SocketServer

from sbd.handler import IridiumTcpHandler

class IridiumServer(SocketServer.TCPServer):

    def __init__(self, host_port, directory):
        SocketServer.TCPServer.__init__(self, host_port, IridiumTcpHandler)
        self._directory = directory

    @property
    def directory(self):
        return self._directory
