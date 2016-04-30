from multiprocessing import Process
from ftp_traverse import Run


d = {
    "1000genomes/": "1000 Genomes Project",
    "dbgap/": "dbGaP",
    "entrez/": "Entrez",
    "genbank/": "GenBank",
    "geo/": "Gene Expression Omnibus",
    "refseq/": "RefSeq",
    "sra/": "Sequence Read Archive",
    "epigenomics/": "Epigenomics Database",
}


address = "ftp.ncbi.nlm.nih.gov"
parts = [d.items()[i:i + 4] for i in range(0, len(d), 4)]

for part in parts:
    for root, name in part:
        processes = []

        print "Start processes ", root, "...\n\n"
        run = Run(name, "ftp.ncbi.nlm.nih.gov", root)
        p = Process(target=run.main_run, args=())
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
