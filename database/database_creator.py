import sqlite3 as lite
import os
import json


conn = lite.connect('PubData.db')
curs = conn.cursor()

for path_, _, files in os.walk("json_files"):
    for file_name in files:
        table_name = file_name.split('.')[0].replace(' ', '_')
        query = """CREATE TABLE {} (id int PRIMARY KEY NOT NULL,
                                    file_path text     NOT NULL,
                                    file_name text     NOT NULL);""".format(table_name)
        curs.execute(query)
        try:
            with open(os.path.join(path_, file_name)) as f:
                result = json.load(f)
        except:
            print "File {} gtes excaped!".format(file_name)
        else:
            id_ = 0
            for path_add, file_names_ in result.items():
                for name in file_names_:
                    id_ += 1
                    conn.execute("""INSERT INTO {} (id, file_path, file_name)
                                    VALUES (?, ?, ?)""".format(table_name), (id_, path_add, name))
            print "File {} successfully gets imported".format(file_name)

    # curs.execute("""CREATE INDEX index_name on table_name (column1, column2);""")
        conn.commit()
