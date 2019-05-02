from collections import namedtuple
from tedutil.dec import dec
from tedutil.accounting.account import Account
from tedutil.accounting.transaction_line import TrLine
from tedutil.accounting.config import CREDIT


class Transaction:
    def __init__(self, date, parastatiko, perigrafi, partner='', type_=1):
        self.type = int(type_)
        self.date = date
        self.par = parastatiko
        self.per = perigrafi
        self.partner = partner
        self.lines = list()

    def add_line(self, account_code, type_, value, partner='', acc_name=None):
        self.lines.append(TrLine(Account(account_code, acc_name),
                                 type_, value, partner))

    def add_final_line(self, account_code):
        lin = TrLine(Account(account_code), CREDIT, self.delta)
        lin.normalize()
        self.lines.append(lin)

    @property
    def to_line(self):
        hed = f"9|{self.type}|{self.date}|{self.par}|{self.per}|{self.partner}"
        lins = []
        for lin in self.lines:
            lins.append(f"{lin.account.code}|{lin.type}|{lin.value}|"
                        f"{lin.partner}")
        tlin = ' ? '.join(lins)
        return hed + " @ " + tlin

    @property
    def size(self):
        return len(self.lines)

    @property
    def total(self):
        return sum([i.debit for i in self.lines])

    @property
    def total_debit(self):
        return sum([i.debit for i in self.lines])

    @property
    def total_credit(self):
        return sum([i.credit for i in self.lines])

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
        st1 = (f"\n{self.date:<10} {self.par:<15} {self.per:<30} "
               f"{self.partner:<10}\n")
        for line in self.lines:
            st1 += line.__str__() + '\n'
        stt = "%-61s %12s %12s"
        st1 += '-' * 87 + '\n'
        st1 += stt % ('Σύνολα', self.total_debit, self.total_debit) + '\n'
        return st1

    def __repr__(self):
        stt = f"Transaction({self.date},{self.par},{self.per},{self.partner})"
        for line in self.lines:
            stt += '\n' + line.__repr__()
        return stt

    def unval(self):
        return f'{self.date}{self.par}{self.size}{self.total}'
