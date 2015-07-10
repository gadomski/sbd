import os

from sbd.server import IridiumServer


class IridiumApp(object):

    PIDFILE_TIMEOUT = 5

    def __init__(self, host, port, directory):
        self.stdin_path = "/dev/null"
        self.stdout_path = os.path.join(directory, "server.stdout")
        self.stderr_path = os.path.join(directory, "server.stderr")
        self.pidfile_path = os.path.join(directory, "server.pid")
        self.pidfile_timeout = self.PIDFILE_TIMEOUT
        self.host = host
        self.port = port
        self.directory = directory
    
    def run(self):
        self.server = IridiumServer((self.host, self.port), self.directory)
        self.server.serve_forever()
