import logging
import os
import SocketServer

from sbd.handler import IridiumTcpHandler

class IridiumServer(SocketServer.TCPServer):

    def __init__(self, host_port, directory):
        SocketServer.TCPServer.__init__(self, host_port, IridiumTcpHandler)
        self._directory = directory
        self._logger = logging.getLogger(__name__)

        handler = logging.FileHandler(os.path.join(self._directory, "server.log"))
        formatter = logging.Formatter("%(levelname)s: %(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def handle_error(self, request, client_address):
        self.logger.exception("Error when handling request from {0}".format(client_address))

    @property
    def directory(self):
        return self._directory

    @property
    def logger(self):
        return self._logger
