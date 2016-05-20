from PySide import QtCore
import ftplib
import os


servers = {"PANTHER": "ftp.pantherdb.org", 
           "miRBase": "mirbase.org", 
           "Ensembl Genome Browser": "ftp.ensembl.org", 
           "Rat Genome Database": "rgd.mcw.edu", 
           "Genomicus": "ftp.biologie.ens.fr", 
           "Human Microbiome Project": "public-ftp.hmpdacc.org", 
           "Protein Information Resource": "ftp.pir.georgetown.edu", 
           "The Arabidopsis Information Resource": "ftp.arabidopsis.org/home", 
           "AAindex": "ftp.genome.jp", 
           "O-GLYCBASE": "ftp.cbs.dtu.dk", 
           "Xenbase": "ftp.xenbase.org", 
           "Pasteur Insitute": "ftp.pasteur.fr", 
           "Uniprot": "ftp.uniprot.org", 
           "Flybase": "ftp.flybase.net", 
           "NECTAR": "ftp.nectarmutation.org", 
           "Global Proteome Machine and Database": "ftp.thegpm.org", 
           "REBASE": "ftp.neb.com", 
           "UCSC Genome Browser": "hgdownload.cse.ucsc.edu", 
           "PairsDB": "nic.funet.fi", 
           "Molecular INTeraction database": "mint.bio.uniroma2.it",
           "National Center for Biotechnology Information": "ftp.ncbi.nlm.nih.gov"}


for server_name, path in servers.items():
    def get_files(connection):
        file_list, dirs, nondirs = [], [], []
        connection.retrlines('LIST', lambda x: file_list.append(x.split()))
        for info in file_list:
            ls_type, name = info[0], info[-1]
            if ls_type.startswith('d'):
                dirs.append(name)
            else:
                nondirs.append(name)
        return dirs, nondirs
    try:
        connection = ftplib.FTP(path)
        connection.login()
    except Exception as exp:
        print "Connection to server {} was unsuccessful. {}".format(server_name, exp)
    else:
        print "Successfully connected to server {}".format(server_name)

        dirs, nondirs = get_files(connection)
        directory = os.path.join("all_meta", server_name)
        os.mkdir(directory)
        if not nondirs and len(dirs) == 1:
            print "change path"
            connection.cwd(dirs[0])
            dirs, nondirs = get_files(connection)
        else:
            pub = next((i for i in dirs if 'pub' in i.lower()), None)
            if pub:
                print "change path"
                connection.cwd(pub)
                dirs, nondirs = get_files(connection)
        try:
            for file_name in nondirs:
                if file_name.endswith(('.txt', '.pdf', '.xml', '.msg')) or 'readme' in file_name.lower():
                    with open(os.path.join(directory, file_name), 'wb') as f:
                        connection.retrbinary("RETR " + file_name, f.write)
        except Exception as exp:
            print exp
        else:
            print "Files {} get downloaded successfully".format(nondirs)