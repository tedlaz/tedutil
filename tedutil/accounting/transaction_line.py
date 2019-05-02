from tedutil.dec import dec
from tedutil.accounting.config import DEBIT
from tedutil.accounting.config import CREDIT


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
        return self.value if self.type == CREDIT else dec(0)

    @property
    def delta(self):
        return self.debit - self.credit

    @property
    def delta_reversed(self):
        return self.credit - self.debit

    def reverse(self):
        if self.type == DEBIT:
            self.type = CREDIT
        elif self.type == CREDIT:
            self.type = DEBIT

    def reversed(self):
        if self.type == DEBIT:
            type_ = CREDIT
        elif self.type == CREDIT:
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
        return f"TrLine(code: {self.account.code}, name: {self.account.name},"\
               f" debit: {self.debit}, credit: {self.credit})"
