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
        payload_file = os.path.join(directory, basename + ".payload")
        sbd_file = os.path.join(directory, basename + ".sbd")

        if os.path.isfile(payload_file) or os.path.isfile(sbd_file):
            self.server.logger.warn("Message recieved at {0} has already been stored, skipping".format(time_of_session))
            return

        with open(payload_file, "wb") as f:
            f.write(message.payload)
        with open(sbd_file, "wb") as f:
            f.write(string.getvalue())

        self.server.logger.info("Message recieved at {0} stored OK".format(time_of_session))
