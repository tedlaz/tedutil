"""Ελληνικοί λογαριασμοί Λογιστικής"""
from collections import namedtuple
from tedutil.dec import dec
from tedutil import acc_parse as acp


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
EE_SET = {PAGIA, APOTHEMATA, EJODA, ESODA}
EE_ESODA = (PAGIA, APOTHEMATA, EJODA)
EE_EJODA = (ESODA,)
EE_FPA = (FPA, PAGIA, APOTHEMATA, EJODA, ESODA)
ACC_NORMAL_STATUS = {
    TAJEOS: 0,
    PAGIA: 1,
    APOTHEMATA: 1,
    APAITHSEIS: 1,
    KEFALAIO: -1,
    YPOXREOSEIS: -1,
    EJODA: 1,
    ESODA: -1,
    APOTELESMATA: 0,
    ANALYTIKH: 0
}

REVAL = {
    '0': 'u',
    '1': 'a',
    '2': 'b',
    '3': 'z',
    '4': 'z',
    '5': 'z',
    '6': 'c',
    '7': 'd',
    '8': 'u',
    '9': 'u'
}

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

    # @property
    # def re(self):
    #     val = ''

    #     if self.account.startswith(FPA):
    #         if self.account.startswith('54.00.9'):
    #             val = 'z'
    #         else:
    #             val = 'v'
    #     else:
    #         val = REVAL.get(self.account[0], 'u')

    #     if self.value < 0:
    #         val = val.upper()

    #     return val

    @property
    def re(self):
        # Το παρακάτω δουλεύει μόνο σε python 3.6 και μετά
        # γιατί παίζει ρόλο η σειρά που διαβάζεται το dict
        # (Θα πρέπει πρώτα να ελεγθούν οι πιο ειδικές περιπτώσεις
        #  πχ 54.00.00.9 και μετά οι πιο γενικές πχ 54.00 και πιο κάτω 5)
        REVAL1 = {
            '54.00.9': 'z',
            '54.00.': 'v',
            '1': 'a',
            '2': 'b',
            '3': 'z',
            '4': 'z',
            '5': 'z',
            '6': 'c',
            '7': 'd',
        }
        val = 'u'
        for key, value in REVAL1.items():
            if self.account.startswith(key):
                val = value
                break
        if self.value < 0:
            val = val.upper()

        return val
    @property
    def value_float(self):
        return round(float(self.value), 2)

    @property
    def value_str(self):
        return str(self.value)

    @property
    def prosimo(self):
        if self.value < 0:
            return 'NEGATIVE'
        return 'POSITIVE'

    @property
    def as_dic(self):
        return {'acc': self.account, 'val': float(self.value)}

    def reverse(self):
        return TransactionLine(self.account, -self.value)

    @property
    def typos(self):
        if self.account.startswith(FPA):
            return 'fpa'
        elif self.account.startswith(EE_ESODA):
            return 'esoda'
        elif self.account.startswith(EE_EJODA):
            return 'ejoda'
        else:
            return 'etc'

    @property
    def omada(self):
        if self.account.startswith(FPA):
            return 'fpa'
        elif self.account[0] in '0123456789':
            return self.account[0]
        else:
            return ''

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
    """Λογιστικό άρθρο
    Περιέχει κινήσεις λογαριασμών.
    Για να είναι σωστό θα πρέπει:
    1. Το σύνολο των γραμμών να είναι μηδέν (Χρεώσεις = Πιστώσεις)
    2. Οι εγγραφές να απεικονίζουν πραγματικές κινήσεις και παραστατικά
       Δεν γίνεται για παράδειγμα να έχουμε εγγραφή τιμολογίου αγορών και
       να υπάρχει λογαριασμός της ομάδας 7 στο άρθρο.
       Οι βασικοί κανόνες είναι οι εξής:
          1. Αγορές-Έξοδα ('1', '2', '6', '54.00')
          2. Πωλήσεις ('7', '54.00')
    """
    def __init__(self, date, parastatiko, perigrafi, afm=''):
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

    @property
    def ee_lines(self):
        if not self.is_ee:
            return None
        for line in self.lines:
            if line.account.startswith(EE_FPA):
                yield line

    @property
    def re(self):
        re_set = set()
        for lin in self.lines:
            re_set.add(lin.re)
        lst = sorted(sorted(list(re_set)), key=str.upper)
        return ''.join(lst)

    @property
    def re_lower(self):
        return self.re.lower()

    @property
    def is_same_sign(self):
        """Αν οι γραμμές με αποτελεσματικούς λ/μούς έχουν το ίδιο πρόσημο ή όχι

        Returns:
            Bool: True, False
        """
        prosima = set()
        for lin in self.ee_lines:
            prosima.add(lin.prosimo)
        return len(prosima) == 1

    @property
    def is_ee(self):
        """Εάν η εγγραφή είναι για το βιβλίο εσόδων/εξόδων
        Για να είναι η εγγραφή για το ΕΕ θα πρέπει:
        Να κινούνται λογαριασμοί από τις ομάδες 1, 2, 6, 7 (EE_SET)
        Returns:
            boolean: True or False
        """
        re_low = self.re_lower
        for flag in 'abcd':
            if flag in re_low:
                return True
        return False

    @property
    def ee_type(self):
        EeType = namedtuple('EeType', 'ee normal_credit per')
        normal = 'normal'
        credit = 'credit'
        error = 'error'
        flg = {
            'Dz': EeType(1, normal,'Πωλήσεις χωρίς ΦΠΑ'),
            'dZ': EeType(1, credit, 'Πιστωτικό πωλήσεων χωρίς ΦΠΑ'),
            'DVz': EeType(1, normal, 'Πωλήσεις με ΦΠΑ'),
            'dvZ': EeType(1, credit, 'Πιστωτικό πωλήσεων με ΦΠΑ'),
            'bZ': EeType(2, normal, 'Αγορές χωρίς ΦΠΑ'),
            'Bz': EeType(2, credit, 'Πιστωτικό αγορών χωρίς ΦΠΑ'),
            'bvZ': EeType(2, normal, 'Αγορές με ΦΠΑ'),
            'BVz': EeType(2, credit, 'Πιστωτικό αγορών χωρίς ΦΠΑ'),
            'cZ': EeType(2, normal, 'Εξοδα χωρίς ΦΠΑ'),
            'Cz': EeType(2, credit, 'Πιστωτικό εξόδων χωρίς ΦΠΑ'),
            'cvZ': EeType(2, normal, 'Εξοδα με ΦΠΑ'),
            'CVz': EeType(2, credit, 'Πιστωτικό εξόδων με ΦΠΑ'),
            'bcZ': EeType(2, normal, 'Αγορές και Εξοδα χωρίς ΦΠΑ'),
            'BCz': EeType(2, credit, 'Πιστωτικό αγορών και εξόδων χωρίς ΦΠΑ'),
            'bcvZ': EeType(2, normal, 'Αγορές και Εξοδα με ΦΠΑ'),
            'BCVz': EeType(2, credit, 'Πιστωτικό αγορών και εξόδων με ΦΠΑ'),
            'Zz': EeType(0, normal, 'Συμψηφιστικές εγγραφές')
        }
        return flg.get(self.re, EeType(-1, error, f'error in {self}'))

    @property
    def is_proper_ee(self):
        print(self.typos_set)
        # Αν το άρθρο δεν είναι ισοσταθμισμένο τότε είναι ούτως ή άλλως λάθος
        if not self.is_ok:
            return False
        # Δεν γίνεται να υπάρχουν έσοδα και έξοδα μαζί σε μία εγγραφή
        if {ESODA, EJODA}.issubset(self.typos_set):
            return False
        # Δεν γίνεται να υπάρχουν έσοδα και αποθέματα μαζί
        if {ESODA, APOTHEMATA}.issubset(self.typos_set):
            return False
        # Θα πρέπει σε ένα άρθρο όλοι οι λογαριασμοί των (1, 2, 54.00, 7)
        # να έχουν το ίδιο πρόσημο
        if not self.is_same_sign:
            return False
        return True

    @property
    def ee_typos(self):
        if not self.is_proper_ee:
            return None
        if APOTHEMATA in self.typos_set:
            return 'ejoda'
        elif EJODA in self.typos_set:
            return 'ejoda'
        elif ESODA in self.typos_set:
            return 'esoda'
        else:
            return 'error'

    @property
    def to_ee(self):
        eetypos = self.ee_typos
        if not eetypos:
            return None
        synt = 1
        esex = 'Εξοδα'
        if eetypos == 'esoda':
            synt = -1
            esex = 'Εσοδα'

        tval = tfpa = 0
        accs = set()
        for lin in self.ee_lines:
            val = lin.value_float * synt
            if lin.omada == 'fpa':
                tfpa += val
            elif lin.omada in EE_SET:
                accs.add(lin.account)
                tval += val
        return {
            'ee': esex,
            'date': self.date,
            'afm': self.afm,
            'par': self.parastatiko,
            'per': self.perigrafi,
            'val': tval,
            'fpa': tfpa,
            'total': tval + tfpa,
            'accs': accs
        }

    @property
    def is_balanced(self):
        return self.is_ok

    @property
    def is_fpa(self):
        """Αν η εγγραφή έχει ΦΠΑ ή όχι

        Returns:
            boolean: True αν έχει ΦΠΑ, false αν δεν έχει ΦΠΑ
        """
        if not self.is_ee:
            return False
        if 'fpa' not in self.typos_set:
            return False
        return True

    @classmethod
    def from_dic(cls, adi):
        trn = cls(
            adi['dat'],
            adi['par'],
            adi['per'],
            adi.get('afm', '')
        )
        for lin in adi['z']:
            trn.add_line(lin['acc'], lin['val'])
        return trn

    @property
    def as_dic(self):
        adi = {
            'dat': self.date,
            'par': self.parastatiko,
            'per': self.perigrafi,
            'afm': self.afm,
            'z': [l.as_dic for l in self.lines]
        }
        return adi

    def reverse(self, date, par):
        per = f"Reversed transaction {self.date}, {self.parastatiko}"
        rev = Transaction(date, par, per, self.afm)
        for lin in self.lines:
            rev.add_line_object(lin.reverse())
        return rev

    def add_line_object(self, tranline: TransactionLine):
        if type(tranline) != TransactionLine:
            raise ValueError(f"{tranline} is not a TransactionLine object")
        self.lines.append(tranline)
        self.total_lines += 1
        self.delta += tranline.value
        self.account_set.add(tranline.account)
        self.typos_set.add(tranline.omada)
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
        """
        """
        return None

    @property
    def endokoinotiki(self):
        return None

    def __repr__(self):
        return (
            f"Transaction(date='{self.date}',"
            f" parastatiko='{self.parastatiko}',"
            f" perigrafi='{self.perigrafi}',"
            f" afm='{self.afm}',"
            f" lines={self.lines})"
        )


class Book:
    def __init__(self, acc_pars):
        self.chart, self.chart0, self.ee = acp.acc_parse(acc_pars)
        self.xrisi = None
        self.transactions = []
        self.account_set = set()
        self.min_date = ''
        self.max_date = ''

    def check_account_validity(self):
        for acc in self.account_set:
            acp.match_account(acc, self.chart)

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
    def as_list_of_dicts(self):
        ldi = []
        for trn in self.transactions:
            ldi.append(trn.as_dic)
        return ldi

    @property
    def number_of_transactions(self):
        return len(self.transactions)

    @property
    def number_of_accounts(self):
        return len(self.account_set)

    def add_trans_from_list_dic(self, ldi):
        for dic in ldi:
            self.add_transaction_object(Transaction.from_dic(dic))

    def add_transaction_object(self, tran_object):

        if type(tran_object) != Transaction:
            raise ValueError(f'{tran_object} is not a Transaction')

        # if not tran_object.date.startswith(self.xrisi):
        #     raise ValueError(f'{tran_object} date is not in {self.xrisi}')

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
        # Η χρήση είναι το έτος της μικρότερης ημερομηνίας
        self.xrisi = self.min_date[:4]
        assert self.min_date[:4] == self.max_date[:4]

    def add_transaction_dict(self, trn: dict) -> None:
        pass

    @property
    def to_ee(self):
        for trn in self.transactions:
            tr2ee = trn.to_ee
            if tr2ee:
                print(tr2ee)

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
