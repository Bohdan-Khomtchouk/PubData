from runwalker import ftpwalker

# "Pasteur Insitute", "ftp.pasteur.fr"
walker = ftpwalker("Uniprot", "ftp.uniprot.org")
# "O-GLYCBASE", "ftp.cbs.dtu.dk"
walker.check_state()
