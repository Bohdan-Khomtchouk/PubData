#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------


import sqlite3 as lite
import os
import json

server_names = {"PANTHER": "ftp.pantherdb.org",
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
                "Gene Expression Omnibus": "ftp.ncbi.nlm.nih.gov/geo",
                "One Thousand Genomes Project": "ftp.ncbi.nlm.nih.gov/1000genomes",
                "dbGaP": "ftp.ncbi.nlm.nih.gov/dbgap",
                "GenBank": "ftp.ncbi.nlm.nih.gov/genbank",
                "Epigenomics Database": "ftp.ncbi.nlm.nih.gov/epigenomics",
                "Sequence Read Archive": "ftp.ncbi.nlm.nih.gov/sra",
                "RefSeq": "ftp.ncbi.nlm.nih.gov/refseq",
                "Entrez": "ftp.ncbi.nlm.nih.gov/entrez"}


def create_servernames_table(servernames):
    print "Creating server names table..."
    conn = lite.connect('PubData.db')
    curs = conn.cursor()
    table_name = "servernames"
    curs.execute("""CREATE TABLE {} (id   INT   PRIMARY KEY NOT NULL,
                                     name text  NOT NULL,
                                     url  text  NOT NULL);""".format(table_name))

    for _id, (name, url) in enumerate(servernames.items(), 1):
        conn.execute("""INSERT INTO {} (id, name, url)
                        VALUES (?, ?, ?)""".format(table_name), (_id, name, url))
    conn.commit()


def database_creator():
    conn = lite.connect('PubData.db')
    curs = conn.cursor()

    for path_, _, files in os.walk("database/json_files"):
        for file_name in files:
            table_name = file_name.split('.')[0].replace(' ', '_')
            if table_name:
                query = """CREATE TABLE {} (id int PRIMARY KEY NOT NULL,
                                            file_path text     NOT NULL,
                                            file_name text     NOT NULL);""".format(table_name)
                curs.execute(query)
                try:
                    with open(os.path.join(path_, file_name)) as f:
                        result = json.load(f)
                except:
                    print "File {} gtes escaped!".format(file_name)
                else:
                    id_ = 0
                    for path_add, file_names_ in result.items():
                        for name in file_names_:
                            id_ += 1
                            conn.execute("""INSERT INTO {} (id, file_path, file_name)
                                            VALUES (?, ?, ?)""".format(table_name), (id_, path_add, name))
                    print "File {} successfully gets imported".format(file_name)

        curs.execute("""CREATE INDEX {}_index on {} (file_path, file_name);""".format(table_name, table_name))
        conn.commit()

def create_wordnet_table():
    conn = lite.connect('PubData.db')
    curs = conn.cursor()
    table_name = "WordNet"

    query = """CREATE TABLE {} (id       int PRIMARY KEY NOT NULL,
                                word     text            NOT NULL,
                                synonyms text            NOT NULL);""".format(table_name)
    curs.execute(query)
    with open("WordNet/corpus_new.json") as f:
        result = json.load(f)

    id_ = 0
    for word, synonyms in result.items():
        id_ += 1
        conn.execute("""INSERT INTO {} (id, word, synonyms)
                        VALUES (?, ?, ?)""".format(table_name), (id_, word, str(synonyms)))
    print "File {} successfully gets imported".format("corpus.json")
    curs.execute("""CREATE INDEX alphabet on {} (word, synonyms);""".format(table_name))
    conn.commit()

def create_recommender_table():
    print "Creating recommender system tables..."
    conn = lite.connect('PubData.db')
    curs = conn.cursor()

    table_name = "recommender_exact"
    query = """CREATE TABLE {} (id   int PRIMARY KEY,
                                word text   NOT NULL UNIQUE,
                                rank text   NOT NULL );""".format(table_name)
    curs.execute(query)
    curs.execute("""CREATE INDEX {}_index on {} (word);""".format(table_name, table_name))
    table_name = "recommender_syns"
    query = """CREATE TABLE {} (id   int PRIMARY KEY,
                                word text   NOT NULL UNIQUE,
                                rank text   NOT NULL);""".format(table_name)
    curs.execute(query)
    curs.execute("""CREATE INDEX {}_index on {} (word);""".format(table_name, table_name))
    conn.commit()


if __name__ == "__main__":
    try:
        create_servernames_table(server_names)
    except Exception as exp:
        print exp
    database_creator()
    create_wordnet_table()
    create_recommender_table()
