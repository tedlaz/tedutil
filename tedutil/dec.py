"""Greek decimal functions"""


from decimal import Decimal
from decimal import ROUND_HALF_UP


def is_number(value):
    """Checks if value is number or not

    :param value: value to be checked
    :return: True/False
    """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(value, decimals=2):
    """Creates a proper decimal

    :param value: number or string representing decimal
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    decimals = int(decimals)
    poso = 0 if (value is None) else value
    tmp = Decimal(poso) if is_number(poso) else Decimal(0)
    return tmp.quantize(Decimal(10) ** (-1 * decimals), rounding=ROUND_HALF_UP)


def dec2gr(poso, decimals=2, zero_as_space=True):
    """Greek formated decimal to string

    :param poso: Python decimal number
    :param decimals: Number of decimal digits
    :param zero_as_space: How to treat zero values
    :return: Greek formatted decimal string
    """
    tpo = dec(poso, decimals)
    fst = '{:,.%sf}' % decimals
    if tpo == 0:
        if zero_as_space:
            return ''
    return fst.format(tpo).replace(",", "X").replace(".", ",").replace("X", ".")


def gr2dec(strval, decimals=2):
    """Greek decimal string to python decimal number

    :param strval: Greek decimal string
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    return dec(strval.replace('.', '').replace(',', '.'), decimals)


def split_val_to_list(val, alist, decimals=2):
    """Splits val according to alist values

    :param val: Value to be splitted
    :param alist: List of values
    :param decimals: Number of decimals
    :return: List of splitted val with length = len(alist) + 1
    """
    lval = []
    rest = dec(val, decimals)
    for step in alist:
        if rest > step:
            lval.append(dec(step, decimals))
            rest -= step
        else:
            lval.append(rest)
            rest = 0
    lval.append(rest)
    return lval


def klimaka(value, scale, percent):
    """Calculate percent of value given scale, percent rate

    :param value: Decimal value
    :param scale:  list of decimal values
    :param percent:  List of decimal values
    :return: Calculated value
    """
    if (len(scale) + 1) != len(percent):
        raise ValueError
    dpercent = [dec(dec(i)/ dec(100), 4) for i in percent]
    vall = split_val_to_list(value, scale)
    pval = [dec(vall[i] * dpercent[i]) for i in range(len(percent))]
    return sum(pval)


def distribute(value, alist, decimals=2):
    """Distributes value according alist distribution

    :param value: Value to be distributed
    :param alist: Distribution list/ tuple
    :param decimals: Decimal places
    :return: Distribution list
    """
    value = dec(value, decimals)
    totald = dec(sum(alist), decimals)
    dist = [dec(value * dec(i, decimals) / totald, decimals) for i in alist]
    rest = value - sum(dist)  # if there is a diff
    dist[dist.index(max(dist))] += rest  # add it to max value
    return dist
