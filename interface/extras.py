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

general_style = """QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}
        QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}
        QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog{border-radius:4px; color:black; font-weight:500; font-size:12pt}"""


SERVER_NAMES = {'Ensembl Genome Browser': 'ftp.ensembl.org',
                'UCSC Genome Browser': 'hgdownload.cse.ucsc.edu',
                'Uniprot': 'ftp.uniprot.org',
                'Flybase': 'ftp.flybase.net',
                'Xenbase': 'ftp.xenbase.org',
                'The Arabidopsis Information Resource': 'ftp.arabidopsis.org/home',
                'Rat Genome Database': 'rgd.mcw.edu',
                'Human Microbiome Project': 'public-ftp.hmpdacc.org',
                'National Center for Biotechnology Information': 'ftp.ncbi.nlm.nih.gov',
                'REBASE': 'ftp.neb.com',
                'NECTAR': 'ftp.nectarmutation.org',
                'Global Proteome Machine and Database': 'ftp.thegpm.org',
                'Protein Information Resource': 'ftp.pir.georgetown.edu',
                'O-GLYCBASE': 'ftp.cbs.dtu.dk',
                'Pasteur Insitute': 'ftp.pasteur.fr',
                'miRBase': 'mirbase.org',
                'Genomicus': 'ftp.biologie.ens.fr',
                'AAindex': 'ftp.genome.jp',
                'PairsDB': 'nic.funet.fi',
                'Molecular INTeraction database': 'mint.bio.uniroma2.it',
                'PANTHER': 'ftp.pantherdb.org'}
