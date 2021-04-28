from dataclasses import dataclass, field
from enum import Enum
import weakref


DeCr = Enum('DeCr', "DEBIT CREDIT")
ACCOUNT_SPLITTER = '.'


class EeLine:
    def __init__(self):
        pass

class Account:
    """Flyweight implementation of account"""
    _pool = weakref.WeakValueDictionary()

    def __new__(cls, code, name=''):
        # If the object exists in the pool - just return it
        obj = cls._pool.get(code)
        # otherwise - create new one (and add it to the pool)
        if obj is None:
            obj = object.__new__(Account)
            cls._pool[code] = obj
            obj.code, obj.name = code, name
        else:
            """Μπορεί να αλλάξει μόνο το όνομα του λογαριασμού"""
            if name:
                obj.name = name
        return obj

    def __repr__(self):
        return f"Account(code='{self.code}', name='{self.name}')"

    @property
    def is_numeric(self):
        """Εάν ο code αποτελείται από αριθμούς και splitter"""
        return self.code.replace(ACCOUNT_SPLITTER, '').isdigit()

    @property
    def tree(self) -> tuple:
        spl = self.code.split(ACCOUNT_SPLITTER)
        lvls = [ACCOUNT_SPLITTER.join(spl[: i + 1]) for i in range(len(spl))]
        if self.is_numeric:
            return [self.code[0]] + lvls
        return tuple(lvls)

    @property
    def level(self) -> int:
        return len(self.code.split(ACCOUNT_SPLITTER))

    @property
    def omada(self) -> str:
        return self.tree[0]


@dataclass(frozen=True)
class TranLine:
    account: Account
    value: float

    @property
    def value_float(self) -> float:
        return round(float(self.value), 2)

    @property
    def value_str(self) -> str:
        return str(self.value)

    @property
    def debit(self) -> float:
        return 0 if self.value < 0 else self.value

    @property
    def credit(self) -> float:
        return -self.value if self.value < 0 else 0

    def new_reversed_tranline(self):
        return TranLine(self.account, -self.value)


@dataclass
class Tran:
    """Άρθρο λογιστικής"""
    date: str
    par: str
    per: str
    afm: str = ''
    lines: list = field(default_factory=list)

    def add_line(self, account: Account, value: float) -> None:
        self.lines.append(TranLine(account, value))

    @property
    def type(self):
        return

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
    def ee(self):
        """Εδώ μετατρέπεται το άρθρο σε γραμμή του βιβλίου εσόδων-εξόδων"""
        pass


class Book:
    def __init__(self, chart0: str):
        self.chart0 = chart0
        self.arthra = []

    def add_transaction(self, arthro) -> None:
        self.arthra.append(arthro)

    def add_transactions_from_json(self, json_file):
        pass

    def isozygio(self, apo: str = None, eos: str = None):
        """Ισοζύγιο περιόδου

        Args:
            apo (date, optional): Από. Defaults to None.
            eos (date, optional): Έως. Defaults to None.

        Returns:
            [type]: [description]
        """
        for trn in self.arthra:
            pass

    def fpa(self, apo, eos):
        """Αναφορά ΦΠΑ περιόδου

        Args:
            apo (date): Από
            eos (date): Έως
        """
        pass

    def kartella(self, account, apo, eos):
        """Καρτέλλα λογαριασμού

        Args:
            account (str): Ο λογαριασμός ή αρχικό μέρος του λογαριασμού
            apo (date): Από
            eos (date): Έως
        """
        pass

    def ee(self, apo, eos):
        """Βιβλίο Εσόδων-Εξόδων"""
        pass

    def myf(self, apo, eos):
        pass

    def imerologio(self, apo, eos):
        pass
