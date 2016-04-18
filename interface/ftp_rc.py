#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.
# Future plans include adding web server support for PubData, and contributions from the open source community are welcome.
# PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PySide (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  
# By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and retrieve files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.
# PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.
# Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------

from PySide import QtCore

qt_resource_data = "\
\x00\x00\x00\x9b\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x00\x48\x00\x00\x00\x48\
\x00\x46\xc9\x6b\x3e\x00\x00\x00\x4d\x49\x44\x41\x54\x38\xcb\x63\
\x60\x18\x34\x60\xe6\xcc\x99\xff\xd1\x31\x49\x9a\xcf\x9c\x39\xf3\
\xff\xff\x7f\x06\x14\x9a\x28\x43\x70\x69\x46\x36\x04\xaf\xeb\x40\
\x1c\x52\x01\xd4\x80\xff\x68\x06\x30\xe0\x75\x09\x32\x8d\xd5\x00\
\x62\x35\x23\x85\xcd\xa8\x0b\xa8\xea\x02\x72\x30\xdc\x00\x28\xf8\
\x4f\x26\xa6\x1c\x00\x00\x8c\xaf\xf9\x48\x94\xb3\xf7\xb4\x00\x00\
\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
\x00\x00\x00\x81\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x04\x00\x00\x00\xb5\xfa\x37\xea\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x00\x48\x00\x00\x00\x48\
\x00\x46\xc9\x6b\x3e\x00\x00\x00\x33\x49\x44\x41\x54\x28\xcf\x63\
\x60\x20\x04\xea\xff\x63\x42\x34\x05\xe8\x60\x3f\xaa\x12\x6c\x0a\
\xfe\x23\x2b\xc1\x54\xc0\x00\x83\xb8\x14\x40\x4c\x19\x55\x80\xa1\
\x60\x3f\x56\x08\x57\xc0\xf0\x1f\x27\x04\x03\x00\x03\xba\x4b\xb1\
\x6c\xf1\xe8\x3e\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
\
\x00\x00\x00\x8b\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x0f\x00\x00\x00\x0d\x08\x06\x00\x00\x00\x76\x1e\x34\x41\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x00\x48\x00\x00\x00\x48\
\x00\x46\xc9\x6b\x3e\x00\x00\x00\x3d\x49\x44\x41\x54\x28\xcf\x63\
\x60\x40\x80\xff\x58\x30\x51\xe0\xff\xff\xff\x33\x31\x30\x31\x06\
\xfc\xa7\x00\x63\xb7\x95\x10\xc6\xa9\x99\x18\x03\xb1\x6a\x46\x76\
\x16\x49\x9a\xb1\xf9\x8b\x7e\xce\xa6\x8a\x66\x42\x5e\xa0\x4d\x54\
\x91\xa4\x99\x5c\x0c\x00\xd4\x48\xc0\x4e\x47\x46\xbd\x51\x00\x00\
\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = "\
\x00\x06\
\x07\x03\x7d\xc3\
\x00\x69\
\x00\x6d\x00\x61\x00\x67\x00\x65\x00\x73\
\x00\x07\
\x0b\x05\x57\x87\
\x00\x64\
\x00\x69\x00\x72\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x08\
\x00\x28\x5a\xe7\
\x00\x66\
\x00\x69\x00\x6c\x00\x65\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x0e\
\x0f\x3b\x9c\x27\
\x00\x63\
\x00\x64\x00\x74\x00\x6f\x00\x70\x00\x61\x00\x72\x00\x65\x00\x6e\x00\x74\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct = "\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x02\
\x00\x00\x00\x26\x00\x00\x00\x00\x00\x01\x00\x00\x00\x9f\
\x00\x00\x00\x12\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x00\x3c\x00\x00\x00\x00\x00\x01\x00\x00\x01\x24\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
