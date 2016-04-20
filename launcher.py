#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import BioNetHub

if __name__ == '__main__':

	file_name=raw_input('Enter the file name')

	BNH=BioNetHub.search(file_name)
	BNH.server_selecter()
	BNH.download()