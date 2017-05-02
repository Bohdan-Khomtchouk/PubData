#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

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

server_names = {"PANTHER": "ftp.pantherdb.org",
                "miRBase": "mirbase.org",
                "Ensembl Genome Browser": "ftp.ensembl.org",
                "Rat Genome Database": "ftp.rgd.mcw.edu",
                "Genomicus": "ftp.biologie.ens.fr",
                "Human Microbiome Project": "public-ftp.hmpdacc.org",
                "Protein Information Resource": "ftp.pir.georgetown.edu",
                # "The Arabidopsis Information Resource": "ftp.arabidopsis.org/home",
                "AAindex": "ftp.genome.jp",
                # "O-GLYCBASE": "ftp.cbs.dtu.dk",
                "Xenbase": "ftp.xenbase.org",
                "Pasteur Insitute": "ftp.pasteur.fr",
                "Uniprot": "ftp.uniprot.org",
                "Flybase": "ftp.flybase.net",
                "NECTAR": "ftp.nectarmutation.org",
                "Global Proteome Machine and Database": "ftp.thegpm.org",
                "REBASE": "ftp.neb.com",
                "UCSC Genome Browser": "hgdownload.cse.ucsc.edu",
                # "PairsDB": "nic.funet.fi",
                "Molecular INTeraction database": "mint.bio.uniroma2.it",
                # "Gene Expression Omnibus": "ftp.ncbi.nlm.nih.gov",
                # "One Thousand Genomes Project": "ftp.ncbi.nlm.nih.gov",
                "dbGaP": "ftp.ncbi.nlm.nih.gov",
                # "GenBank": "ftp.ncbi.nlm.nih.gov",
                "Epigenomics Database": "ftp.ncbi.nlm.nih.gov",
                # "Sequence Read Archive": "ftp.ncbi.nlm.nih.gov",
                "RefSeq": "ftp.ncbi.nlm.nih.gov",
                "Entrez": "ftp.ncbi.nlm.nih.gov"}