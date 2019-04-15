from enum import Enum
from tedutil.grtext import grup
from tedutil.dec import dec
# from tedutil.logger import logger


class COL(Enum):
    """FIL is special because it is always empty"""
    TXT = 0  # text
    INT = 1  # integer
    DEC = 2  # decimal
    DAT = 3  # date
    FIL = 4  # filler with spaces
    FI0 = 5  # filler with zeroes


class ROW(Enum):
    """If SUM then row is actually a sum row"""
    NOR = 0  # Normal
    SUM = 1  # Sum


class ColumnTyp:
    """Column type """
    def __init__(self, data):
        self.name, self.size, self.typ, *_ = data

    def render(self, cval):
        """Column rendering occurs here

        :param cval: value to render
        :return: String
        """
        tst = grup(str(cval))
        dif = self.size - len(tst)
        if self.typ == COL.FIL:
            return ' ' * self.size
        elif self.typ == COL.FI0:
            return '0' * self.size
        elif self.typ == COL.TXT:
            return (tst[:self.size]) if dif < 0 else tst + (' ' * dif)
        elif self.typ == COL.DAT:
            return (tst[:self.size]) if dif < 0 else tst + (' ' * dif)
        elif self.typ == COL.INT:
            return ('0' * self.size) if dif < 0 else ('0' * dif) + tst
        elif self.typ == COL.DEC:
            inte, deci = str(dec(cval)).split(".")
            indc = inte + deci
            dif2 = self.size - len(indc)
            return indc[:self.size] if dif2 < 0 else ('0' * dif2) + indc
        return None

    def __str__(self):
        return "%-30s %3s %20s" % (self.name, self.size, self.typ)


class RowTyp:
    def __init__(self, lid, name, typ, columntypes):
        self.id = lid
        self.name = name
        self.typ = typ
        self.columns = [ColumnTyp(data) for data in columntypes]

    def render(self, data):
        """It actually renders the row

        :param data: dictionary of data
        :return: String
        """
        stt = f'{self.id}'
        for col in self.columns:
            val = data.get(col.name, '')
            stt += col.render(val)
        return stt

    def __str__(self):
        stt = f"RowTyp id: {self.id} name: {self.name} typ: {self.typ}\n"
        stt += "columns: \n"
        stt += '\n'.join(col.__str__() for col in self.columns)
        return stt

    def size(self):
        """Returns the size of row"""
        return len(str(self.id)) + sum([i.size for i in self.columns])


class Row:
    def __init__(self, row_typ, data=None):
        self.row_typ = row_typ
        self.data = data or {}

    def render(self):
        """Passes rendering to RowTyp"""
        return self.row_typ.render(self.data)

    def size(self):
        """Returns the size of the final row"""
        return len(self.render())


class Document:
    """Document object"""
    def __init__(self):
        self.rows = []
        self.totals = {}

    def add(self, row):
        """Adds a new row and calculates self.totals
           for decimal and integer values

        :param row: a Row instance
        """
        self.rows.append(row)
        if row.row_typ == ROW.SUM:
            return
        for col in row.row_typ.columns:
            if col.typ == COL.INT:
                val = row.data.get(col.name, 0)
                self.totals[col.name] = self.totals.get(col.name, 0) + int(val)
            elif col.typ == COL.DEC:
                val = dec(row.data.get(col.name, 0))
                self.totals[col.name] = self.totals.get(col.name, 0) + val

    def calc_totals(self):
        """Inserts totals in rows with ROWTYPE.SUM
            totals are already calculated during add()
        """
        for row in self.rows:
            if row.row_typ.typ != ROW.SUM:
                continue
            for col in row.row_typ.columns:
                if col.typ in (COL.DEC, COL.INT):
                    row.data[col.name] = self.totals.get(col.name, 0)

    def render(self):
        """Renders the final text"""
        self.calc_totals()
        stt = ''
        stt += '\n'.join([r.render() for r in self.rows])
        return stt
