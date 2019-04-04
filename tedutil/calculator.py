"""Spreadsheet like functionality"""


from collections import defaultdict
from decimal import Decimal
from functools import reduce
from .dec import dec
from .dec import is_number as isn
# from .utils import calcforos
# from .utils import calceea


def calculator(algorithm, data, des=6):
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
        # elif operator == 'f':  #  Εδώ μπαίνουν συναρτήσεις
        #     _, _, strfunct, *_ = lin.split()
        #     funct = fun[strfunct]
        #     vrs[key] = dec(funct(*par[1:]), decim)
        else:
            raise ValueError('Error in line : %s' % lin)
    return vrs
