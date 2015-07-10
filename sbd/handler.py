import datetime
import os
import SocketServer
import StringIO

from sbd import MobileOriginatedMessage
from sbd.util import mkdir_p


class IridiumTcpHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        string = StringIO.StringIO(self.rfile.read())
        message = MobileOriginatedMessage.parse(string)
        time_of_session = datetime.datetime(1970, 1, 1, 0, 0, 0) + \
                datetime.timedelta(seconds=message.time_of_session)

        directory = os.path.join(self.server.directory, message.imei,
                str(time_of_session.year), "%02d" % time_of_session.month)
        mkdir_p(directory)
        basename = time_of_session.strftime("%y%m%d_%H%M%S")

        with open(os.path.join(directory, basename + ".payload"), "wb") as f:
            f.write(message.payload)
        with open(os.path.join(directory, basename + ".sbd"), "wb") as f:
            f.write(string.getvalue())
