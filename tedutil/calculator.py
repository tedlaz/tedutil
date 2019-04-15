"""Spreadsheet like functionality"""


from collections import defaultdict
from collections import namedtuple
from functools import lru_cache
import os
from decimal import Decimal
from functools import reduce
from tedutil.dec import dec
from tedutil.dec import is_number as isn
# from tedutil.decorators import memoize
# from .utils import calcforos
# from .utils import calceea

Alg = namedtuple('Alg', "operator decimals result parameters")


@lru_cache()
def load_algorithm(algorithm, default_decimals=6):
    algorithm_lines = []
    allowed_operators = tuple("=%*/+->^?dDfF")
    if os.path.isfile(algorithm):
        with open(algorithm, encoding="utf8") as fil:
            adata = fil.read()
    else:
        adata = algorithm
    lines = adata.split('\n')
    if len(lines) == 1:
        raise ValueError("%s is neither existing file or valid string" % adata)
    for lin in lines:
        if len(lin) < 3:
            continue
        elif lin.startswith('#'):
            continue
        elif lin.startswith(allowed_operators):
            (operator, *ldecimals), value, *params = lin.upper().split()
            if len(ldecimals) == 0:
                decimals = default_decimals
            elif len(ldecimals) == 1:
                decimals = ldecimals[0]
                if not decimals.isdigit():
                    raise ValueError("decimal value must be digit %s" % lin)
            else:
                raise ValueError("Wrong number of decimals in %s " % (lin))

            algorithm_lines.append(Alg(operator, decimals, value, params))
        else:
            raise ValueError("Wrong operator %s in line %s" % (lin[0], lin))
    return algorithm_lines



def calc2(algorithm, data, function_dict=None, decimals=6):
    alg_lines = load_algorithm(algorithm)
    dvl = defaultdict(Decimal)
    for key, val in data.items():
        dvl[key.upper()] = Decimal(val)
    for lin in alg_lines:
        dc = lin.decimals
        res = lin.result
        par = lin.parameters
        if lin.operator == '=':
            dvl[res] = dec(par[0] if isn(par[0]) else dvl[par[0]], dc)
        elif lin.operator == '%':
            pr1 = dec(par[0] if isn(par[0]) else dvl[par[0]], dc)
            dvl[res] = dec(pr1 / dec(100), dc)
        elif lin.operator == '*':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            dvl[res] = dec(reduce((lambda x, y: x * y), pr1), dc)
        elif lin.operator == '/':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            dvl[res] = dec(pr1[0] / pr1[1], dc)
        elif lin.operator == '+':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            dvl[res] = dec(sum(pr1), dc)
        elif lin.operator == '-':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            pr2 = [i for i in pr1[1:]]  # αντιστρέφω το πρόσημο
            dvl[res] = dec(pr1[0] - sum(pr2), dc)
        elif lin.operator == '>':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            dif = dec(pr1[0] - pr1[1], dc)
            dvl[res] = dif if dif > 0 else dec(0)
        elif lin.operator == '^':
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par]
            dif = dec(abs(pr1[0] - pr1[1]), dc)
            dvl[res] = dif if dif > pr1[2] else dec(0)
        elif lin.operator.upper() == 'D':
            dvl[res] = dec(dvl[res], dc)
        elif lin.operator == '?':
            par.append(res)
            spar = set(par)
            sinp = set([i.upper() for i in data.keys()])
            if not spar.issubset(sinp):
                raise ValueError('Απαιτουνται %s και δόθηκαν %s' % (spar, sinp))
        elif lin.operator.upper() == 'F':
            strfunct = par[0]
            pr1 = [Decimal(i) if isn(i) else dvl[i] for i in par[1:]]
            funct = function_dict[strfunct]
            dvl[res] = funct(*pr1)
        else:
            raise ValueError('Error in line : %s' % lin.operator)
    return dvl


def calculator(algorithm, data, function_dict=None, des=6):
    alg_lines = algorithm.split('\n')
    vrs = defaultdict(Decimal)
    for key, value in data.items():
        vrs[key] = dec(value, des)
    for lin in alg_lines:
        if len(lin.strip()) < 3:
            continue
        if lin.startswith('#'):
            continue
        operator, key, *dat = lin.split()
        psize = len(dat)
        par = []
        # Εδώ δημιουργούμε δεκαδικές τιμές είτε καλούμε μεταβλητές που υπάρχουν
        for el in dat:
            par.append(dec(el, des) if isn(el) else vrs[el])
        # Απο εδώ ξεκινάει ο υπολογισμός
        if len(operator) == 2:
            decim = int(operator[1])
            operator = operator[0]
        else:
            decim = des
        # print(operator, decim)
        if operator == '=' and psize == 1:  # Iσότητα δύο μεταβλητές
            vrs[key] = dec(par[0], decim)
        elif operator == '%' and psize == 1:
            vrs[key] = dec(par[0] / dec(100), decim)
        elif operator == '*':
            vrs[key] = dec(reduce((lambda x, y: x * y), par), decim)
        elif operator == '/' and psize == 2:
            vrs[key] = dec(par[0] / par[1], decim)
        elif operator == '+':
            vrs[key] = dec(sum(par), decim)
        elif operator == '-' and psize == 2:
            vrs[key] = dec(par[0] - par[1], decim)
        elif operator == '>' and psize == 2:
            dif = dec(par[0] - par[1], decim)
            vrs[key] = dif if dif > 0 else dec(0)
        elif operator == '^' and psize == 3:
            dif = dec(abs(par[0] - par[1]), decim)
            vrs[key] = dif if dif > par[2] else dec(0)
        elif operator == 'd' and psize == 0:  # Στρογγυλοποίηση σε δεκαδικά
            vrs[key] = dec(vrs[key], decim)
        elif operator == '?':
            # Απαιτούμενες παράμετροι εισόδου
            _, *sdata = lin.split()
            spar = set(sdata)
            sinp = set(data.keys())
            if not spar.issubset(sinp):
                raise ValueError('Απαιτουνται %s και δόθηκαν %s' % (spar, sinp))
        elif operator == 'f':  #  Εδώ μπαίνουν συναρτήσεις
            _, _, strfunct, *_ = lin.split()
            funct = function_dict[strfunct]
            vrs[key] = funct(*par[1:])
            del vrs[strfunct]  # Διαγράφουμε από το dictionary τη συνάρτηση
        else:
            raise ValueError('Error in line : %s' % lin)
    return vrs
