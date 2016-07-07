#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------

from ftp_traverse import main_walker

class MainUpdate:
    def __init__(self, servers):
        self.servers = servers

    def update_all(self):
        wkr = main_walker.main_walker(servers=self.servers)
        wkr.walker()

    def update_manual(self, manual_servers):
        servers = {k: v for k, v in self.servers.items() if k in manual_servers}
        wkr = main_walker.main_walker(servers=servers)
        wkr.walker()
