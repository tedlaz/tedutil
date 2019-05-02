from operator import attrgetter
from collections import namedtuple
from collections import defaultdict
from tedutil.dec import dec
from tedutil.grdate import date_out_of_interval
from tedutil.accounting.company import Company
from tedutil.accounting.transaction import Transaction
from tedutil.accounting.levels import levels
from tedutil.accounting.config import FPA
from tedutil.accounting.config import INC


class Book:
    def __init__(self, company_afm, company_name, book_name=None,
                 chart_of_accounts=None, partners=None):
        self.company = Company(company_afm, company_name)
        self.name = book_name
        self.chart = chart_of_accounts or dict()
        self.partners = partners or dict()
        self.trans = list()
        self.unique = set()

    def to_lines(self):
        lines = [f"0|{self.company.afm}|{self.company.name}|{self.name}"]
        for tran in sorted(self.trans, key=attrgetter('date')):
            lines.append(tran.to_lines())
        return "\n".join(lines)

    def uncomplete_transactions(self):
        uncompleted = list()
        for tran in self.trans:
            if not tran.is_complete:
                uncompleted.append(tran)
        return uncompleted

    def save_transaction_to_book(self, transaction):
        uval = transaction.unval()
        if uval in self.unique:
            raise ValueError(f"Transaction {transaction} already exists!!")
        if transaction.is_complete:
            self.unique.add(uval)
            self.trans.append(transaction)
        else:
            raise ValueError(f'Transaction {transaction} is incomplete')

    def new_tran_from_dic(self, trdic):
        tr0 = Transaction(trdic['date'], trdic['par'], trdic['per'])
        for lin in trdic['lines']:
            tr0.add_line(lin['code'], lin['type'], lin['value'])
        self.save_transaction_to_book(tr0)

    def new_tran_from_tuple(self, trtup):
        tr0 = Transaction(trtup.date, trtup.par, trtup.per)
        for lin in trtup.lines:
            tr0.add_line(lin.code, lin.type, lin.value)
        self.save_transaction_to_book(tr0)

    def isozygio(self, date_from='', date_to='', as_tuple=True):
        date_to = '2999-12-31' if date_to == '' else date_to
        res = defaultdict(lambda: {'adebit': dec(0),
                                   'acredit': dec(0),
                                   'adelta': dec(0),
                                   'bdebit': dec(0),
                                   'bcredit': dec(0),
                                   'bdelta': dec(0),
                                   'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)
                                   })
        for tran in self.trans:
            for lin in tran.lines:
                for acc in lin.account.levels:
                    if tran.type == 0:
                        res[acc]['adebit'] += lin.debit
                        res[acc]['acredit'] += lin.credit
                        res[acc]['adelta'] += lin.delta
                    elif tran.type == 1:
                        if tran.date < date_from:
                            res[acc]['bdebit'] += lin.debit
                            res[acc]['bcredit'] += lin.credit
                            res[acc]['bdelta'] += lin.delta
                        elif tran.date <= date_to:
                            res[acc]['debit'] += lin.debit
                            res[acc]['credit'] += lin.credit
                            res[acc]['delta'] += lin.delta
        if not as_tuple:
            return dict(res)
        tuple_list = list()
        Iso = namedtuple('Iso', ['code',
                                 'adebit', 'acredit', 'adelta',
                                 'bdebit', 'bcredit', 'bdelta',
                                 'debit', 'credit', 'delta'])
        for key in sorted(res.keys()):
            tuple_list.append(Iso(key,
                                  res[key]['adebit'],
                                  res[key]['acredit'],
                                  res[key]['adelta'],
                                  res[key]['bdebit'],
                                  res[key]['bcredit'],
                                  res[key]['bdelta'],
                                  res[key]['debit'],
                                  res[key]['credit'],
                                  res[key]['delta']
                                  ))
        return tuple_list

    def isozygio_print(self, date_from='', date_to=''):
        print(f"Isozygio for {self.company} from: {date_from} to: {date_to}")
        iso = self.isozygio(date_from, date_to)
        accounts_without_name = []
        for lin in iso:
            acn = self.chart.get(lin.code, '')
            if acn == '':
                accounts_without_name.append(lin.code)
            tde = lin.adebit + lin.bdebit + lin.debit
            tcr = lin.acredit + lin.bcredit + lin.credit
            tdl = tde - tcr
            aa = 9
            print(f"{lin.code:<15} {acn:<30} "
                  f"{lin.adebit:>{aa}} {lin.acredit:>{aa}} {lin.adelta:>{aa}} "
                  f"{lin.bdebit:>{aa}} {lin.bcredit:>{aa}} {lin.bdelta:>{aa}} "
                  f"{lin.debit:>{aa}} {lin.credit:>{aa}} {lin.delta:>{aa}} "
                  f"{tde:>{aa}} {tcr:>{aa}} {tdl:>{aa}}")
        print("accounts without name : ", accounts_without_name)

    def isozygio_fpa(self, date_from=None, date_to=None):
        res = defaultdict(lambda: dec(0))
        for tran in self.trans:
            if date_out_of_interval(tran.date, date_from, date_to):
                continue
            for lin in tran.lines:
                if lin.account.code.startswith(FPA):
                    res['fpa'] += lin.delta
                elif lin.account.code.startswith(INC):
                    res[lin.account.code] += lin.delta_reversed
                else:
                    res[lin.account.code] += lin.delta
        return res

    def isozygio_partner(self, account_list=None,
                         date_from=None, date_to=None):
        tuple_account_list = tuple(account_list) if account_list else None
        res = defaultdict(lambda: {'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)})
        for tran in self.trans:
            if date_out_of_interval(tran.date, date_from, date_to):
                continue
            for lin in tran.lines:
                key = lin.account.code
                if account_list:
                    if lin.account.code.startswith(tuple_account_list):
                        if lin.partner:
                            key = lin.account.code + '.' + lin.partner
                        elif tran.partner:
                            key = lin.account.code + '.' + tran.partner
                else:
                    if lin.partner:
                        key = lin.account.code + '.' + lin.partner
                    elif tran.partner:
                        key = lin.account.code + '.' + tran.partner
                for keyl in levels(key):
                    res[keyl]['debit'] += lin.debit
                    res[keyl]['credit'] += lin.credit
                    res[keyl]['delta'] += lin.delta
        return res

    def isozygio_partner_print(self, account=None):
        print(f"Isozygio partner for {self.company}")
        iso = self.isozygio_partner(account)
        for key in sorted(iso):
            print(f"{key:<20} {iso[key]['debit']:>12} "
                  f"{iso[key]['credit']:>12} {iso[key]['delta']:>12}")

    def isozygio_kinoymenon(self, date_from=None, date_to=None,
                            as_tuple=False):
        res = defaultdict(lambda: {'debit': dec(0),
                                   'credit': dec(0),
                                   'delta': dec(0)})
        for tran in self.trans:
            if date_out_of_interval(tran.date, date_from, date_to):
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
            acc = self.chart.get(key, '')
            print(f"{key:<15} {acc:<30}{isk[key]['debit']:>12} "
                  f"{isk[key]['credit']:>12} {isk[key]['delta']:>12}")

    def journal_print(self, date_from=None, date_to=None):
        print(f"\nJournal for {self.company.name} ({self.name}):")
        for tran in sorted(self.trans, key=attrgetter('date')):
            if date_out_of_interval(tran.date, date_from, date_to):
                continue
            print(tran)

    def kartella(self, account_code, date_from=None, date_to=None):
        lines = list()
        for tran in sorted(self.trans, key=attrgetter('date')):
            if date_out_of_interval(tran.date, date_from, date_to):
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

    def to_lines(self):
        for tran in self.trans:
            print(tran.to_line)

    def __add__(self, another_book):
        name = self.name + " + " + another_book.name
        new_book = Book(self.company.afm, self.company.name, name,
                        {**self.chart, **another_book.chart},
                        {**self.partners, **another_book.partners})
        new_book.trans = self.trans + another_book.trans
        return new_book

    # def __sub__(self, another_book):
    #     name = self.name + " - " + another_book.name
    #     new_book = Book(self.company.afm, self.company.name, name,
    #                     self.chart, self.partners)
    #     new_book.trans = self.trans + [i.reversed()
    #                                    for i in another_book.trans]
    #     return new_book

    def __repr__(self):
        return f'Book(company: {self.company}, name: {self.name})'
