import sqlite3


def dict_factory(cursor, row):
    adic = {}
    for idx, col in enumerate(cursor.description):
        adic[col[0]] = row[idx]
    return adic


def get_dict(sql, dbfile):
    res = None
    with sqlite3.connect(dbfile) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
    return res


def test1():
    con = sqlite3.connect(":memory:")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("create table tst(man text, woman text)")
    cur.execute("insert into tst values('ted', 'popi')")
    cur.execute("insert into tst values('nikos', 'kyriaki')")
    cur.execute("select * from tst")
    print(cur.fetchall())

