#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

from FTPwalker.runwalker import ftpwalker


def update(server_name, url):
    walker = ftpwalker(server_name, url, daemon=True)
    status = walker.chek_state()
    return status
