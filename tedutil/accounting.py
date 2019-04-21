"""Greek accounting module"""
# from enum import Enum
from collections import namedtuple
from collections import defaultdict
from operator import attrgetter
from tedutil.dec import dec
ACCSPLIT = '.'
ACCTOTAL = '9'
DEBIT, CREDT = 1, 2


def levels(account):
    spl = account.split(ACCSPLIT)
    ranks = [ACCSPLIT.join(spl[:i + 1]) for i in range(len(spl))]
    if spl[0].isdigit() and len(spl[0]) > 1:
        return tuple([ACCTOTAL, spl[0][0]] + ranks)
    return tuple([ACCTOTAL] + ranks)


class Account:
    def __init__(self, code, name=None):
        self.code = code
        self.name = name or ''

    @property
    def levels(self):
        return levels(self.code)

    def __repr__(self):
        return r"Account(code: {self.code}, name: {self.name})"


class TrLine:
    def __init__(self, account, type_, value, partner=''):
        self.account = account
        self.type = type_
        self.value = dec(value)
        self.partner = partner

    @property
    def debit(self):
        return self.value if self.type == DEBIT else dec(0)

    @property
    def credit(self):
        return self.value if self.type == CREDT else dec(0)

    @property
    def delta(self):
        return self.debit - self.credit

    @property
    def delta_reversed(self):
        return self.credit - self.debit

    def reverse(self):
        if self.type == DEBIT:
            self.type = CREDT
        elif self.type == CREDT:
            self.type = DEBIT

    def reversed(self):
        if self.type == DEBIT:
            type_ = CREDT
        elif self.type == CREDT:
            type_ = DEBIT
        else:
            type_ = None
        return TrLine(self.account, type_, self.value, self.partner)

    def normalize(self):
        if self.value < 0:
            self.value = -self.value
            self.reverse()

    def __str__(self):
        return f"{self.account.code:<20} {self.account.name:<30} " \
               f"{self.partner:<9} {self.debit:>12} {self.credit:>12}"

    def __repr__(self):
        return f"TrLine(code: {self.account.code}, name: {self.account.name}, "\
               f"debit: {self.debit}, credit: {self.credit})"


class Transaction:
    def __init__(self, date, parastatiko, perigrafi, partner=None):
        self.date = date
        self.par = parastatiko
        self.per = perigrafi
        self.partner = partner or ''
        self.lines = list()

    def add_line(self, account_code, type_, value, partner=None, acc_name=None):
        self.lines.append(TrLine(Account(account_code, acc_name),
                                 type_, value, partner))

    def add_final_line(self, account_code):
        lin = TrLine(Account(account_code), CREDT, self.delta)
        lin.normalize()
        self.lines.append(lin)

    @property
    def size(self):
        return len(self.lines)

    @property
    def total(self):
        return sum([i.debit for i in self.lines])

    @property
    def delta(self):
        delta = dec(0)
        for line in self.lines:
            delta += line.delta
        return delta

    @property
    def is_complete(self):
        """To be complete:
           1. Must have at least two transaction lines
           2. Must be balanced

        :return: Boolean
        """
        if self.size < 2 or self.delta != 0:
            return False
        return True

    def get_lines_by_code(self, account_code):
        TLi = namedtuple('TLi', "date par per code name debit credit")
        lines = list()
        for line in self.lines:
            if line.account.code.startswith(account_code):
                lines.append(TLi(self.date, self.par, self.per,
                                 line.account.code, line.account.name,
                                 line.debit, line.credit))
        return lines

    def get_lines_by_name(self, account_name):
        return [l for l in self.lines
                if l.account.name.startswith(account_name)]

    def reversed(self):
        per = self.per + " reversed"
        trn = Transaction(self.date, self.par, per, self.partner)
        for lin in self.lines:
            trn.lines.append(lin.reversed())
        return trn

    def __str__(self):
        st1 = f"{self.date} {self.par} {self.per} {self.partner}\n"
        for line in self.lines:
            st1 += line.__str__() + '\n'
        return st1

    def __repr__(self):
        return f"Transaction({self.date}, {self.par}, {self.per}, " \
               f"{self.partner})"

    def unval(self):
        return f'{self.date}{self.par}{self.size}{self.total}'


class Company:
    def __init__(self, afm, name):
        self.afm = afm
        self.name = name
        self.type = None
        self.city = ''

    def __repr__(self):
        return f"Company(afm: {self.afm}, name: {self.name})"


class Book:
    def __init__(self, company, type_, name=None, chart_of_accounts=None):
        self.company = company
        self.type = type_
        self.name = name
        self.chart = chart_of_accounts or dict()
        self.trans = list()
        self.unique = set()

    def uncomplete_transactions(self):
        uncompleted = list()
        for tran in self.trans:
            if not tran.is_complete:
                uncompleted.append(tran)
        return uncompleted

    def new_transaction(self, transaction):
        uval = transaction.unval()
        if uval in self.unique:
            raise ValueError(f"Transaction {transaction} already exists!!")
        self.unique.add(uval)
        self.trans.append(transaction)

    def new_tran_from_dic(self, trdic):
        tr0 = Transaction(trdic['date'], trdic['par'], trdic['per'])
        for lin in trdic['lines']:
            tr0.add_line(lin['code'], lin['type'], lin['value'])
        self.new_transaction(tr0)

    def new_tran_from_tuple(self, trtup):
        tr0 = Transaction(trtup.date, trtup.par, trtup.per)
        for lin in trtup.lines:
            tr0.add_line(lin.code, lin.type, lin.value)
        self.new_transaction(tr0)

    def load_from_file(self, filename):
        with open(filename, encoding='utf8') as file:
            lines = file.read().split('\n')
        add_lines(self, lines)


    def isozygio(self, date_from=None, date_to=None, as_tuple=True):
        res = defaultdict(lambda: {'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)})
        for tran in self.trans:
            if date_from:
                if not (date_from <= tran.date):
                    continue
            if date_to:
                if not (date_to >= tran.date):
                    continue
            for lin in tran.lines:
                for acc in lin.account.levels:
                    res[acc]['debit'] += lin.debit
                    res[acc]['credit'] += lin.credit
                    res[acc]['delta'] += lin.delta
        if not as_tuple:
            return dict(res)
        tuple_list = list()
        Iso = namedtuple('Iso', "code debit credit delta")
        for key in sorted(res.keys()):
            tuple_list.append(Iso(key,
                                  res[key]['debit'],
                                  res[key]['credit'],
                                  res[key]['delta']
                                  ))
        return tuple_list

    def isozygio_print(self):
        print(f"Isozygio for {self.company}")
        iso = self.isozygio()
        for lin in iso:
            print(f"{lin.code:<20} {lin.debit:>12} {lin.credit:>12} "
                  f"{lin.delta:>12}")

    def isozygio_partner(self, account_list=None):
        res = defaultdict(lambda: {'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)})
        for tran in self.trans:
            for lin in tran.lines:
                if account_list:
                    if lin.account.code.startswith(tuple(account_list)):
                        if lin.partner:
                            key = lin.account.code + '.' + lin.partner
                        elif tran.partner:
                            key = lin.account.code + '.' + tran.partner
                        else:
                            key = lin.account.code
                    else:
                        key = lin.account.code
                else:
                    if lin.partner:
                        key = lin.account.code + '.' + lin.partner
                    elif tran.partner:
                        key = lin.account.code + '.' + tran.partner
                    else:
                        key = lin.account.code
                for keyl in levels(key):
                    res[keyl]['debit'] += lin.debit
                    res[keyl]['credit'] += lin.credit
                    res[keyl]['delta'] += lin.delta
        return res

    def isozygio_partner_print(self, account=None):
        print(f"Isozygio partner for {self.company}")
        iso = self.isozygio_partner(account)
        for key in sorted(iso):
            print(f"{key:<20} {iso[key]['debit']:>12} {iso[key]['credit']:>12} "
                  f"{iso[key]['delta']:>12}")

    def isozygio_kinoymenon(self, date_from=None, date_to=None, as_tuple=False):
        res = defaultdict(lambda: {'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)})
        for tran in self.trans:
            if date_from:
                if not (date_from <= tran.date):
                    continue
            if date_to:
                if not (date_to >= tran.date):
                    continue
            for lin in tran.lines:
                res[lin.account.code]['debit'] += lin.debit
                res[lin.account.code]['credit'] += lin.credit
                res[lin.account.code]['delta'] += lin.delta
        if not as_tuple:
            return dict(res)
        tuple_list = list()
        Iso = namedtuple('Iso', "code debit credit delta")
        for key in sorted(res.keys()):
            tuple_list.append(Iso(key,
                                  res[key]['debit'],
                                  res[key]['credit'],
                                  res[key]['delta']
                                  ))
        return tuple_list

    def isozygio_kinoymenon_print(self):
        print(f"Company: {self.company}, Book: {self.name}")
        isk = self.isozygio_kinoymenon()
        for key in sorted(isk.keys()):
            print(f"{key:<20} {isk[key]['debit']:>12} {isk[key]['credit']:>12} "
                  f"{isk[key]['delta']:>12}")

    def journal_print(self, date_from=None, date_to=None):
        print(f"\nJournal for {self.company.name} ({self.name}):")
        for tran in sorted(self.trans, key=attrgetter('date')):
            if date_from:
                if not date_from <= tran.date:
                    continue
            if date_to:
                if not date_to >= tran.date:
                    continue
            print(tran)

    def kartella(self, account_code, date_from=None, date_to=None):
        lines = list()
        for tran in sorted(self.trans, key=attrgetter('date')):
            if date_from:
                if not date_from <= tran.date:
                    continue
            if date_to:
                if not date_to >= tran.date:
                    continue
            lines += tran.get_lines_by_code(account_code)
        return lines

    def myf(self, year):
        """Creates xml myf file"""
        pass

    def fpa(self, date_from, date_to):
        """Creates fpa report for period"""
        pass

    def profit_loss(self, date_from, date_to):
        pass

    def __add__(self, another_book):
        name = self.name + " + " + another_book.name
        new_book = Book(self.company, 'metafora', name)
        new_book.trans = self.trans + another_book.trans
        return new_book

    def __sub__(self, another_book):
        name = self.name + " - " + another_book.name
        new_book = Book(self.company, 'metafora', name)
        new_book.trans = self.trans + [i.reversed() for i in another_book.trans]
        return new_book

    def __repr__(self):
        return f'Book(company: {self.company}, type: {self.type}, ' \
               f'name: {self.name})'


def add_lines(book, lines):
    for lin in lines:
        if len(lin) < 5:
            continue
        ldata = (i.strip() for i in lin.split('|'))
        if lin.startswith('1'):
            _, date, par, per, partner, *_ = ldata
            trx = Transaction(date, par, per, partner)
        elif lin.startswith('2'):
            _, code, type_, value, *rest = ldata
            partner = rest[0] if len(rest) > 0 else ''
            if partner and trx.partner:
                raise ValueError("Partner can only be at line or head")
            trx.add_line(code, int(type_), dec(value), partner)
        elif lin.startswith('9'):
            _, code, type_, value, *rest = ldata
            partner = rest[0] if len(rest) > 0 else ''
            if partner and trx.partner:
                raise ValueError("Partner can only be at line or head")
            trx.add_line(code, int(type_), dec(value), partner)
            book.new_transaction(trx)
        elif lin.startswith('3'):
            _, date, lapo, lse, val, par, per, partner, *_ = ldata
            trb = Transaction(date, par, per, partner)
            trb.add_line(lapo, CREDT, val, partner)
            trb.add_line(lse, DEBIT, val, partner)
            book.new_transaction(trb)
    uncomplete = book.uncomplete_transactions()
    if uncomplete:
        raise ValueError(f'Uncomplete transactions: {uncomplete}')


def book_from_file(filename):
    """first line of file starts with 0 and contains company and book info
    lines starting with:
        1, contain Transaction header data
        2, contain Transaction line data
        3, contain full binary Transaction (Transaction with 2 lines)
    :param filename: file name
    :return: book object
    """
    with open(filename, encoding='utf8') as file:
        text = file.read()
    lines = iter(text.split('\n'))
    book_data = [i.strip() for i in next(lines).split('|')]
    assert book_data[0] == '0'
    _, afm, cname, type_, name, *_ = book_data
    book = Book(Company(afm, cname), type_, name)
    add_lines(book, lines)
    return book
