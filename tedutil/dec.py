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
    except TypeError:
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


def dec2gr(poso, decimals=2):
    """Greek formated decimal to string

    :param poso: Python decimal number
    :param decimals: Number of decimal digits
    :return: Greek formatted decimal string
    """
    def triades(txt, separator='.'):
        ltxt = len(txt)
        rem = ltxt % 3
        prec_space = 3 - rem
        stxt = ' ' * prec_space + txt
        a = []
        while len(stxt) > 0:
            a.append(stxt[:3])
            stxt = stxt[3:]
        a[0] = a[0].strip()
        fval = ''
        for el in a:
            fval += el + separator
        return fval[:-1]
    if dec(poso) == 0:
        return ''
    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    val = dec(strposo, decimals)
    timi = '%s' % val
    if val == 0:
        prosimo = ''
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def gr2dec(strval, decimals=2):
    """Greek decimal string to python decimal number

    :param strval: Greek decimal string
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    return dec(strval.replace('.', '').replace(',', '.'), decimals)
