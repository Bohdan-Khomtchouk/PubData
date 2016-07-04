from multiprocessing import Pool
from ftp_traverse import Run
from datetime import datetime
import json
from collections import OrderedDict
from os import path as ospath

d = {"1000genomes/": "1000 Genomes Project",
     "dbgap/": "dbGaP",
     "entrez/": "Entrez",
     "genbank/": "GenBank",
     "geo/": "Gene Expression Omnibus",
     "hapmap/": "HapMap",
     "refseq/": "RefSeq",
     "sra/": "Sequence Read Archive",
     "epigenomics/": "Epigenomics Database"}

test = {"/dbgap/": "dbGaP"}
# "National Center for Biotechnology Information": "ftp.ncbi.nlm.nih.gov"

for root, name in test.items():
    run = Run(name, "ftp.ncbi.nlm.nih.gov", root)
    base, leadings = run.find_leading(root, thread_flag=False)
    path, _ = base[0]
    leadings = [ospath.join(path, i.strip('/')) for i in leadings]
    print ("Root's leadings are: ", leadings)

    try:
        pool = Pool()
        pool.map(run.main_run, leadings)
    except Exception as exp:
        print(exp)
    else:
        print ('***' * 5, datetime.now(), '***' * 5)
        l = []
        print ('creating list...')
        while run.all_path.qsize() > 0:
            l.append(run.all_path.get())
        print ('creating dict...')
        d = OrderedDict(base + l)
        print ('writing to json...')
        with open('{}.json'.format(name), 'w') as fp:
            json.dump(d, fp, indent=4)
