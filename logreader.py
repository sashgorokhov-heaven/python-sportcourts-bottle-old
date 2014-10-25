import time
import base64

import dbutils


def print_row(row):
    line = '[{}] {} "{} {}"'.format(*row[1:5])
    if row[6]:
        line += ' uid={}'.format(row[6])
    print(line)
    if row[7]:
        print('#' * 50)
        print()
        try:
            print('\t\t', row[7])
        except:
            print(ascii(row[7]))
        try:
            print('\t\t', row[2])
        except:
            print(ascii(row[2]))
        print()
        try:
            print(base64.b64decode(row[9].encode()).decode())
        except:
            print_row(ascii(base64.b64decode(row[9].encode()).decode()))
        print('#' * 50, flush=True)
        print()


with dbutils.dbopen(**dbutils.logsdb_connection) as db:
    last_id = db.execute("SELECT MAX(id) FROM access;")[0][0]
    while True:
        rows = db.execute("SELECT * FROM access WHERE id>{}".format(last_id))
        if len(rows) > 0:
            for row in rows:
                print_row(row)
            last_id = rows[-1][0]
        time.sleep(1)