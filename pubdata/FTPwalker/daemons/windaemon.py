from .winservice import Service, instart
import win32serviceutil


class Daemon(Service):
    def __setattr__(self, name, value):
        setattr(name, value)

    def start(self):
        pass

    def stop(self):
        self.log("I'm done")


def initialize(executable, *args):
    Daemon.start = lambda self: executable(*args)


def start(executable, *args):
    initialize(executable, *args)
    instart(Daemon, 'FTPwalker', 'FTPwalker', stay_alive=False)


def stop():
    import os
    os.system("sc delete FTPwalker")
