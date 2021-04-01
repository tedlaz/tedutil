"""Ελληνικοί λογαριασμοί Λογιστικής"""
from tedutil.dec import dec


TAJEOS = '0'
PAGIA = '1'
APOTHEMATA = '2'
APAITHSEIS = '3'
KEFALAIO = '4'
YPOXREOSEIS = '5'
EJODA = '6'
ESODA = '7'
APOTELESMATA = '8'
ANALYTIKH = '9'
FPA = '54.00'
EE_SET = {'1', '2', '6', '7'}

"""
Για κάθε εγγραφή σε κάθε περίπτωση έχουμε:
PAGIA+APOTHEMATA+APAITHSEIS+KEFALAIO+YPOXREOSEIS+EJODA+ESODA+APOTELESMATA=0
Γιά εγγραφές πωλήσεων ESODA+APAITHSEIS+YPOXREOSEIS=0
Γιά εγγραφές αγορών PAGIA+APTHEMATA+APAITHSEIS+YPOXREOSEIS=0
Το κέρδος χρήσης προκύπτει από:
APOTHEMATA+EJODA+ESODA πλέον τη διαφορά της απογραφής
"""

class Account:
    def __init__(self, code, per=None):
        self.code = code
        self.per = per

    @property
    def levels(self):
        return levels(self.code)

    @property
    def levels_reverse(self):
        return levels_reverse(self.code)

    def __repr__(self):
        return f"Account(code={self.code}, per={self.per})"


class TransactionLine:
    def __init__(self, account, value):
        self.account = account
        if value == 0:
            raise ValueError("Δεν μπορεί να είναι μηδενικό το value")
        self.value = dec(value)

    @property
    def typos(self):
        if self.account.startswith(FPA):
            return 'fpa'
        if self.account[0] in '12345678':
            return self.account[0]
        return 'err'

    @property
    def debit(self):
        return self.value if self.value > 0 else dec(0)

    @property
    def credit(self):
        return dec(0) if self.value >= 0 else -self.value

    @property
    def debit_negative(self):
        return self.value if self.value < 0 else dec(0)

    @property
    def credit_negative(self):
        return dec(0) if self.value < 0 else -self.value

    def __repr__(self):
        return f"TransactionLine(account='{self.account}', value={self.value})"


class Transaction:
    def __init__(self, date, parastatiko, perigrafi, afm=None):
        self.date = date
        self.parastatiko = parastatiko
        self.perigrafi = perigrafi
        self.afm = afm
        self.lines = []
        self.total_lines = 0
        self.delta = 0
        self.is_ok = False
        self.account_set = set()
        self.typos_set = set()

    def add_line_object(self, tranline: TransactionLine):
        if type(tranline) != TransactionLine:
            raise ValueError(f"{tranline} is not a TransactionLine object")
        self.lines.append(tranline)
        self.total_lines += 1
        self.delta += tranline.value
        self.account_set.add(tranline.account)
        self.typos_set.add(tranline.typos)
        if self.total_lines > 1 and self.delta == 0:
            self.is_ok = True
        else:
            self.is_ok = False

    def add_line(self, account, value):
        self.add_line_object(TransactionLine(account, value))

    def add_lines(self, lines):
        for lin in lines:
            if len(lin) == 1:
                self.add_final_line(lin[0])
            else:
                self.add_line(*lin)

    def add_final_line(self, account):
        if self.total_lines == 0:
            raise ValueError("Θα πρέπει να υπάρχει τουλάχιστον μία γραμμή")
        if self.delta == 0:
            raise ValueError("Το άρθρο είναι ήδη ισοσκελισμένο")

        self.add_line(account, -self.delta)
        self.is_ok = True

    @property
    def myf(self):
        return None

    @property
    def is_fpa(self):
        if not self.is_ee:
            return False
        if 'fpa' not in self.typos_set:
            return False
        return True

    @property
    def is_ee(self):
        if not self.typos_set.intersection(EE_SET):
            return False
        return True

    @property
    def endokoinotiki(self):
        return None

    def __repr__(self):
        return (
            f"Transaction(date='{self.date}',"
            f" parastatiko='{self.parastatiko}',"
            f" perigrafi='{self.perigrafi}',"
            f" lines={self.lines})"
        )


class Book:
    def __init__(self, xrisi: str):
        self.xrisi = str(xrisi)
        self.transactions = []
        self.account_set = set()
        self.min_date = ''
        self.max_date = ''

    def trans_filter_by_date(self, apo=None, eos=None):
        for tran in self.transactions:
            if apo and tran.date < apo:
                continue
            if eos and tran.date > eos:
                continue

            yield tran

    def trans_filter_by_type(self, typos, apo=None, eos=None):
        for tran in self.trans_filter_by_date(apo, eos):
            if tran.type == typos:
                yield tran

    def trans_ee(self, apo=None, eos=None):
        for tran in self.trans_filter_by_date(apo, eos):
            if tran.is_ee:
                yield tran

    @property
    def number_of_transactions(self):
        return len(self.transactions)

    @property
    def number_of_accounts(self):
        return len(self.account_set)

    def add_transaction_object(self, tran_object):

        if type(tran_object) != Transaction:
            raise ValueError(f'{tran_object} is not a Transaction')

        if not tran_object.date.startswith(self.xrisi):
            raise ValueError(f'{tran_object} date is not in {self.xrisi}')

        if not tran_object.is_ok:
            raise ValueError(f'{tran_object} is not balanced')

        self.transactions.append(tran_object)
        self.account_set = self.account_set.union(tran_object.account_set)

        # Αποθήκευση ελάχιστης και μέγιστης ημερομηνίας transaction
        if self.min_date == '':
            self.min_date = tran_object.date
            self.max_date = tran_object.date

        if tran_object.date > self.max_date:
            self.max_date = tran_object.date
        if tran_object.date < self.min_date:
            self.min_date = tran_object.date
    def add_transaction_dict(self, trn: dict) -> None:
        pass

    def __repr__(self):
        return (
            f"Book(xrisi='{self.xrisi}',"
            f" numberOfTransactions={self.number_of_transactions},"
            f" numberOfAccounts={self.number_of_accounts},"
            f" minDate='{self.min_date}', maxDate='{self.max_date}'"
            ")"
        )


def levels_list(account: str, splitter='.') -> list:
    """Από έναν λογαριασμό μας επιστρέφει λίστα με επίπεδα:
       10.00.00 -> [1, 10, 10.00, 10.00.00]

    Args:
        account (str): Ο λογαριασμός
        splitter (str, optional): Το διαχωριστικό με προεπιλεγμένη τιμή το '.'

    Returns:
        list: Λίστα με υπολογαριασμούς από τον ανώτερο έως τον αρχικό
    """
    spl = account.split(splitter)
    lvls = [splitter.join(spl[: i + 1]) for i in range(len(spl))]
    if account[0] in '0123456789':
        return [account[0]] + lvls
    return lvls


def levels(account: str, splitter='.') -> tuple:
    """Από έναν λογαριασμό μας επιστρέφει tuple με επίπεδα:
       38.00.01 -> (3, 38, 38.00, 38.00.01)

    Args:
        account (str): Ο λογαριασμός
        splitter (str, optional): Το διαχωριστικό με προεπιλεγμένη τιμή το '.'

    Returns:
        tuple: Λίστα με υπολογαριασμούς από τον ανώτερο έως τον αρχικό
    """
    return tuple(levels_list(account, splitter))


def levels_reverse(account: str, splitter='.') -> tuple:
    """Από έναν λογαριασμό μας επιστρέφει αντεστραμμένη tuple με επίπεδα:
       38.00.01 -> (38.00.01, 38.00, 38, 3)

    Args:
        account (str): Ο λογαριασμός
        splitter (str, optional): Το διαχωριστικό με προεπιλεγμένη τιμή το '.'

    Returns:
        tuple: Λίστα με υπολογαριασμούς από τον αρχικό έως τον ανώτερο
    """
    levelsl = levels_list(account, splitter)
    levelsl.reverse()
    return tuple(levelsl)


# def read_chart(chart_file):
#     """
#     Δημιουργεί dictionary με τους ανωτεροβάθμιους λογαριασμούς του
#     λογιστικού σχεδίου της μορφής : {'38.00': 'Ταμείο', ...}
#     """
#     chart = {}
#     if os.path.exists(chart_file):
#         with open(chart_file) as fil:
#             for lin in fil.readlines():
#                 if len(lin.strip()) < 3:
#                     continue
#                 acc, *name = lin.split()
#                 chart[acc.strip()] = ' '.join(name)
#     else:
#         raise (f'chart file {chart_file} does not exist. Check your ini')
#     return chart
