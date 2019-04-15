import sqlite3
from collections import namedtuple


def dict_factory(cursor, row):
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


def get_dict(sql, db_file):
    # res = None
    with sqlite3.connect(db_file) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
    return res


def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def get_namedtuple(sql, db_file):
    with sqlite3.connect(db_file) as con:
        con.row_factory = namedtuple_factory
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
    return res


'''
def test1():
    con = sqlite3.connect(":memory:")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("create table tst(man text, woman text)")
    cur.execute("insert into tst values('ted', 'popi')")
    cur.execute("insert into tst values('nikos', 'kyriaki')")
    cur.execute("select * from tst")
    print(cur.fetchall())


def test2():
    con = sqlite3.connect(":memory:")
    con.row_factory = namedtuple_factory
    cur = con.cursor()
    cur.execute("create table tst(man text, woman text)")
    cur.execute("insert into tst values('ted', 'popi')")
    cur.execute("insert into tst values('nikos', 'kyriaki')")
    cur.execute("select * from tst")
    print(cur.fetchall())
'''
