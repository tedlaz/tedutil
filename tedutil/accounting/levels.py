from tedutil.accounting.config import ACCSPLIT
from tedutil.accounting.config import ACCTOTAL


def levels(account):
    spl = account.split(ACCSPLIT)
    ranks = [ACCSPLIT.join(spl[:i + 1]) for i in range(len(spl))]
    if spl[0].isdigit() and len(spl[0]) > 1:
        return tuple([ACCTOTAL, spl[0][0]] + ranks)
    return tuple([ACCTOTAL] + ranks)
