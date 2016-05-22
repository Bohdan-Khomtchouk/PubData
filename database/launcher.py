from multiprocessing import Process
from ftp_traverse import Run
import os


d = {"geo/": "Gene Expression Omnibus",
     "sra/": "Sequence Read Archive"}


# "National Center for Biotechnology Information": "ftp.ncbi.nlm.nih.gov",
address = "ftp.ncbi.nlm.nih.gov"

run = Run("Gene Expression Omnibus", "ftp.ncbi.nlm.nih.gov", "geo/")

(base, files), leadings = run.find_leading()

parts = [leadings[i:i + 4] for i in range(0, len(d), 4)]

for part in parts:
    print part
    for root in part:
        processes = []
        root = os.path.join(base, root.strip('/'))
        print "Start processes ", root, "...\n\n"
        run = Run("Gene Expression Omnibus", "ftp.ncbi.nlm.nih.gov", root)
        p = Process(target=run.main_run, args=())
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
