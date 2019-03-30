from decimal import Decimal
from decimal import ROUND_HALF_UP


def is_number(value):
    """Checks if value is number or not

    :param value:
    :return:
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


def dec2gr(poso, decimals=2, zeroAsSpace=True):
    """Greek formated decimal to string

    :param poso: Python decimal number
    :param decimals: Number of decimal digits
    :return: Greek formatted decimal string
    """
    tpo = dec(poso, decimals)
    fst = '{:,.%sf}' % decimals
    if tpo == 0:
        if zeroAsSpace:
            return ''
    return fst.format(tpo).replace(",", "X").replace(".", ",").replace("X", ".")


def gr2dec(strval, decimals=2):
    """Greek decimal string to python decimal number

    :param strval: Greek decimal string
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    return dec(strval.replace('.', '').replace(',', '.'), decimals)


def klimaka(value, scale, percent):
    """

    :param value: Decimal value
    :param scale:  list of decimal values
    :param percent:  List of decimal values
    :return:
    """
    if len(scale) + 1 != len(percent):
        raise ValueError
    d100 = dec(100)
    rest = dec(value)
    total = dec(0)
    for i, step in enumerate(scale):
        if rest > step:
            total += dec(dec(step) * dec(percent[i]) / d100)
            rest -= step
        else:
            total += dec(rest * dec(percent[i]) / d100)
            rest = 0
            break
    total += dec(rest * dec(percent[-1]) / d100) if rest != 0 else dec(0)
    return total
