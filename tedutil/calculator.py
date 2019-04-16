from collections import defaultdict
from collections import namedtuple
from functools import lru_cache
import os
from decimal import Decimal
from tedutil.dec import dec
from tedutil.dec import is_number
from tedutil.dec import dec_with_given_digits
from tedutil.taxes import foros_periodoy
from tedutil.taxes import eea_periodoy


def calcdispatch(fn):
    registry = dict()

    def register(symbol):
        def inner(fn):
            registry[symbol.upper()] = fn
            return fn

        return inner

    def decorator(*arg):
        if arg[0].upper() not in registry:
            raise ValueError(
                "Symbol %s not in registry (args: %s)" % (arg[0], arg))
        fun = registry[arg[0].upper()]
        return fun(*arg[1:])

    def registered():
        return tuple(registry.keys())

    decorator.register = register
    decorator.registered = registered
    return decorator


Alg = namedtuple('Alg', "operator decimals result pars")


@lru_cache()
def load_algorithm(algorithm):
    algorithm_lines = []
    # allowed = tuple("=%*/+->^?dDfF")
    if os.path.isfile(algorithm):
        with open(algorithm, encoding="utf8") as fil:
            adata = fil.read()
    else:
        adata = algorithm
    lines = adata.split('\n')
    for lin in lines:
        if len(lin) < 3 or lin.startswith('#') or lin.startswith(' '):
            continue
        operator, decimals, value, *params = lin.upper().split()
        algorithm_lines.append(Alg(operator, decimals, value, params))
    return algorithm_lines


def calculate(alg_lines, data):
    res = defaultdict(Decimal)
    for key, val in data.items():
        res[key.upper()] = dec_with_given_digits(val)
    for el in alg_lines:
        args = [dec(i) if is_number(i) else res[i] for i in el.pars]
        res[el.result] = dec(calc(el.operator, args), el.decimals)
    return res


# Start creating calculator's operations
@calcdispatch
def calc():
    return 0


@calc.register('=')
def _(arg):
    return arg[0]


@calc.register('%')
def _(arg):
    return arg[0] / dec(100)


@calc.register('/')
def _(arg):
    return arg[0] / arg[1]


@calc.register('*')
def _(arg):
    mult = 1
    for el in arg:
        mult = mult * el
    return mult


@calc.register('+')
def _(vlist):
    return sum(vlist)


@calc.register('-')
def _(arg):
    return arg[0] - sum(arg[1:])


@calc.register('>')
def _(arglist):
    dif = arglist[0] - arglist[1]
    return dif if dif > 0 else 0


@calc.register('^')
def _(alist):
    dif = abs(alist[0] - alist[1])
    return dif if dif >= alist[2] else 0


@calc.register('foros')
def _(alist):
    # 2019 FOROLOGITEO PAIDIA BARYTIS-PERIODOY
    etos, forologiteo, paidia, barytis, *_ = alist
    return foros_periodoy(etos, forologiteo, paidia, barytis)


@calc.register('eea')
def _(alist):
    # 2019 FOROLOGITEO PAIDIA BARYTIS-PERIODOY
    etos, forologiteo, barytis, *_ = alist
    return eea_periodoy(etos, forologiteo, barytis)
