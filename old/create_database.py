import sqlite3
import os
from parser_text import parse


def create_database(filename):
    dbname = f"{filename}.sql3"
    if os.path.exists(dbname):
        raise FileExistsError(f'{dbname} exists')
    sq1 = ("CREATE TABLE lmo("
           "id INTEGER PRIMARY KEY, "
           "lmos TEXT UNIQUE"
           ");"
           "CREATE TABLE trn("
           "id INTEGER PRIMARY KEY, "
           "date DATE, "
           "par TEXT, "
           "per TEXT"
           ");"
           "CREATE TABLE trnd("
           "id INTEGER PRIMARY KEY, "
           "trn_id INTEGER NOT NULL REFERENCES trn(id), "
           "lmo_id INTEGER NOT NULL REFERENCES lmo(id), "
           "val NUMERIC NOT NULL DEFAULT 0"
           ");"
           "CREATE VIEW vtrn AS "
           "SELECT trn.id, trn.date, trn.par, trn.per, lmo.lmos, trnd.val "
           "from trn "
           "inner join trnd on trn.id=trnd.trn_id "
           "inner join lmo on lmo.id=trnd.lmo_id;"
           )
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.executescript(sq1)
    res = parse(filename)
    lmoi, trn, trnd = prepare(res)
    cur.executemany("INSERT INTO lmo VALUES(?,?)", lmoi)
    cur.executemany("INSERT INTO trn VALUES(?,?,?,?)", trn)
    cur.executemany("INSERT INTO trnd VALUES(?,?,?,?)", trnd)
    con.commit()
    cur.close()
    con.close()


def prepare(res):
    lmois = []
    for account, acc_id in res['accounts_ids'].items():
        lmois.append((acc_id, account))
    trns = []
    trnds = []
    for trn in res['transactions']:
        trns.append((trn['id'], trn['date'], trn['par'], trn['per']))
        for lin in trn['lines']:
            trnds.append(
                (lin['id'], trn['id'], lin['acc_id'], float(lin['value'])))
    return lmois, trns, trnds


if __name__ == '__main__':
    print(create_database('tedata'))
