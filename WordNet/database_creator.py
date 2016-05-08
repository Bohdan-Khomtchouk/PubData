#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import sqlite3 as lite
import json


conn = lite.connect('../database/PubData.db')
curs = conn.cursor()


table_name = "WordNet"

query = """CREATE TABLE {} (id       int PRIMARY KEY NOT NULL,
                            word     text            NOT NULL,
                            synonyms text            NOT NULL);""".format(table_name)
curs.execute(query)

with open("corpus.json") as f:
    result = json.load(f)

id_ = 0
for word, synonyms in result.items():
    id_ += 1
    conn.execute("""INSERT INTO {} (id, word, synonyms)
                    VALUES (?, ?, ?)""".format(table_name), (id_, word, str(synonyms)))
print "File {} successfully gets imported".format("corpus.json")

curs.execute("""CREATE INDEX alphabet on {} (word, synonyms);""".format(table_name))
conn.commit()
