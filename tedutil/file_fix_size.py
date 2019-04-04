"""Create fixed size data files"""


from enum import Enum
from .grtext import grup
from .dec import dec


class COLTYPE(Enum):
    TXT = 0
    INT = 1
    DEC = 2
    DAT = 3
    FIL = 4


def fill(value, size, typos):
    """

    :param value:
    :param size:
    :param typos:
    :return:
    """
    value = grup(str(value))
    vsize = len(value)
    if vsize > size:
        print("Warning field size exeeds line field size")
        value = value[:size]
        vsize = size
    empty = size - vsize
    if typos in 'D':
        return '0' * empty + value
    elif typos == 'S':
        return value + empty * ' '
    else:
        raise ValueError('Value: %s, Invalid typos : %s' % (value, typos))


class Line:
    def __init__(self, stt):
        self.fields = stt.split()
        self.types = [fld[0] for fld in self.fields]
        self.sizes = [int(fld[1:]) for fld in self.fields]
        self.line_size = sum(self.sizes)
        self.number_of_fields = len(self.fields)

    def render(self, data):
        res = ''
        for i, elm in enumerate(self.fields):
            res += fill(data[i], self.sizes[i], self.types[i])
        return res + '\n'


def make_file(data):
    ln1 = "S1 S8 S8 D4 S127"
    ln2 = "D1 D4 S18 S9 S3 D1 D9 S16 S10 S16 S5 D5 D2 S49"
    ln3 = "D1 D16 D16 D16 D15 D15 D15 D14 D13 S27"
    ln4 = "D1 D9 S1 S18 S9 S3 S11 D2 D2 D11 D10 D11 " \
          "D1 S2 D2 D5 D10 D10 D9 D8 D4 D4 S1 D4"
    li1 = Line(ln1)
    li2 = Line(ln2)
    li3 = Line(ln3)
    li4 = Line(ln4)
    fin = li1.render(data['l1'])
    fin += li2.render(data['l2'])
    fin += li3.render(data['l3'])
    for lin4 in data['l4']:
        fin += li4.render(lin4)
    # with open('sss.txt', 'w', encoding='windows-1253') as fil:
    #     fil.write(fin)
    return fin


class Column:
    def __init__(self, name, size, typos, ref=(None, None)):
        self.name = name
        self.size = size
        self.type = typos
        self.line_name, self.col_name = ref

    def render(self, cval):
        tst = grup(str(cval))
        dif = self.size - len(tst)
        if self.type == COLTYPE.FIL:
            return ' ' * self.size
        elif self.type == COLTYPE.TXT:
            return (tst[:self.size]) if dif < 0 else tst + (' ' * dif)
        elif self.type == COLTYPE.DAT:
            return (tst[:self.size]) if dif < 0 else tst + (' ' * dif)
        elif self.type == COLTYPE.INT:
            return ('0' * self.size) if dif < 0 else ('0' * dif) + tst
        elif self.type == COLTYPE.DEC:
            inte, deci = str(dec(cval)).split(".")
            indc = inte + deci
            dif2 = self.size - len(indc)
            return indc[:self.size] if dif2 < 0 else ('0' * dif2) + indc
        return None

    def __str__(self):
        return f"{self.name} {self.size} {self.type}"


class Row:
    def __init__(self, id, name, typos):
        self.id = id
        self.name = name
        self.type = typos
        self.columns = {}
        self.column_names = []
        self.col_set = set()
        self.col_ref = None

    def add_column_object(self, column):
        if column.name in self.column_names:
            raise ValueError("Column name < %s > already exists" % column.name)
        self.column_names.append(column.name)
        if column.type != COLTYPE.FIL:
            self.col_set.add(column.name)
        self.columns[column.name] = column

    def new_column(self, rname, rsize, rtypos):
        self.add_column_object(Column(rname, rsize, rtypos))

    @property
    def size(self):
        tmp = sum([self.columns[nam].size for nam in self.column_names])
        return tmp + len(str(self.id))

    def render(self, dval):
        ftx = str(self.id)  # Πρώτα βάζουμε τον αριθμό τύπου γραμμής
        for cname in self.column_names:
            if cname in dval.keys():
                ftx += self.columns[cname].render(dval[cname])
            else:
                ftx += self.columns[cname].render('')
        return ftx

    def __str__(self):
        return f"Row(name={self.name}, type={self.type})"


class Document:
    def __init__(self):
        self.row_templates = {}
        self.templ_names = []
        self.lines = []
        self.totals = {}

    def add_row_template(self, rowtmpl):
        if rowtmpl.name in self.templ_names:
            raise ValueError("Template %s already exists" % rowtmpl.name)
        self.templ_names.append(rowtmpl.name)
        self.row_templates[rowtmpl.name] = rowtmpl

    def add_row_templates(self, *rowtemplates):
        for rowtmpl in rowtemplates:
            self.add_row_template(rowtmpl)

    def adl(self, line):
        """Για να γίνει δεκτή γραμμή θα πρέπει να υπάρχουν όλα τα απαραίτητα
        πεδία του αντιστοιχου row_template

        :param line:
        :return:
        """
        if line['n4m'] not in self.templ_names:
            raise ValueError("Template %s does not exist" % line['n4m'])
        lset = set(line.keys())
        cset = self.row_templates[line['n4m']].col_set
        if not cset.issubset(lset) and self.row_templates[line['n4m']].type == 0:
            raise ValueError("%s is not subset of %s" % (cset, lset))
        self.lines.append(line)
        for key, val in line.items():
            if key in cset:
                cty = self.row_templates[line['n4m']].columns[key].type
                if cty == COLTYPE.DEC or cty == COLTYPE.INT:
                    self.totals[key] = self.totals.get(key, 0) + val

    def render(self):
        txtl = []
        for lin in self.lines:
            tname = lin['n4m']
            if self.row_templates[tname].type == 1:
                lin2 = {**self.totals, **lin}
                txtl.append(self.row_templates[tname].render(lin2))
            else:
                txtl.append(self.row_templates[tname].render(lin))
        return '\n'.join(txtl)
