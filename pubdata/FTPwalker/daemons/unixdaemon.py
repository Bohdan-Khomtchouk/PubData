"""
=====
daemon.py
=====

Daemon service for Unix based platforms.
Inspired by: http://code.activestate.com/recipes/66012-fork-a-daemon-process-on-unix/
============================

"""

# -*- coding: utf-8 -*-

import sys
import os
import time
from signal import SIGTERM


class Daemon:
    """
    ==============

    ``Daemon``
    ----------

    .. py:class:: Daemon()

    """
    def __init__(self, stdout='/dev/null', stderr=None, stdin='/dev/null'):
        """
        .. py:attribute:: __init__()


           :param stdout:
           :type stdout:
           :param stderr:
           :type stderr:
           :param stdin:
           :type stdin:
           :rtype: None
        """
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.startmsg = 'started with pid {}'

    def deamonize(self, pidfile=None):
        """
        .. py:attribute:: deamonize()

        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null. You can change it
        to something like '/tmp/deamonize.log' if you need to track the stdout.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.

           :param pidfile:
           :type pidfile:
           :rtype: None

        """
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # Exit first parent.
        except OSError as exc:
            sys.stderr.write("fork #1 failed: ({}) {}\n".format(exc.errno, exc.self.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # Exit second parent.
        except OSError as exc:
            print(exc)
            sys.stderr.write("fork #2 failed: ({}) {}\n".format(exc.errno, exc.self.strerror))
            sys.exit(1)

        # Open file descriptors and print start message
        if not self.stderr:
            self.stderr = self.stdout
        pid = str(os.getpid())
        sys.stderr.write("\n{}\n".format(self.startmsg.format(pid)))
        sys.stderr.flush()
        if pidfile:
            with open(pidfile, 'w+') as f:
                f.write("{}\n".format(pid))

    def startstop(self, action, pidfile='pid.txt'):
        """
        .. py:attribute:: startstop()


           :param action:
           :type action:
           :param pidfile:
           :type pidfile:
           :rtype: None

        """
        try:
            with open(pidfile) as pf:
                pid = int(pf.read().strip())
        except (IOError, ValueError):
            pid = None
        if 'stop' == action or 'restart' == action:
            if not pid:
                mess = "Could not stop, pid file '{}' missing.\n"
                sys.stderr.write(mess.format(pidfile))
                sys.exit(1)
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(1)
            except OSError as exc:
                exc = str(exc)
                if exc.find("No such process") > 0:
                    os.remove(pidfile)
                    if 'stop' == action:
                        sys.exit(0)
                    action = 'start'
                    pid = None
                else:
                    print(str(exc))
                    sys.exit(1)
        elif 'start' == action:
            if pid:
                mess = "Start aborded since pid file '{}' exists.\n"
                sys.stderr.write(mess.format(pidfile))
                sys.exit(1)
            self.deamonize(pidfile)
            return
        sys.exit(2)


    def start(self, function, *args):
        """
        .. py:attribute:: run()

           :param function:
           :type function:
           :rtype: None

        """
        print("Start unix daemon...")
        self.startstop("start", pidfile='/tmp/deamonize.pid')
        if function:
            function(*args)
    def stop(self):
        """
        .. py:attribute:: run()

           :rtype: None

        """
        print("Stop unix daemon...")
        self.startstop("stop", pidfile='/tmp/deamonize.pid')
