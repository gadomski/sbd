import SocketServer

from sbd.handler import IridiumTcpHandler

class IridiumServer(SocketServer.TCPServer):

    def __init__(self, host_port, target_directory):
        SocketServer.TCPServer.__init__(self, host_port, IridiumTcpHandler)
        self._target_directory = target_directory

    @property
    def target_directory(self):
        return self._target_directory
