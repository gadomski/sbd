import datetime
import os
import SocketServer
import StringIO

from sbd import MobileOriginatedMessage
from sbd.util import mkdir_p


class IridiumTcpHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        now = datetime.datetime.utcnow()
        directory = os.path.join(self.server.target_directory, str(now.year), "%02d" % now.month)
        mkdir_p(directory)
        basename = now.strftime("%y%m%d_%H%M%S")
        string = StringIO.StringIO(self.rfile.read())
        message = MobileOriginatedMessage.parse(string)
        with open(os.path.join(directory, basename + ".txt"), "wb") as f:
            f.write(message.data)
        with open(os.path.join(directory, basename + ".sbd"), "wb") as f:
            f.write(string.getvalue())
