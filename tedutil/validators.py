"""Greek VAT and Social Security Number validation functions"""
from datetime import date


def is_afm(afm):
    """Algorithmic check for greek vat numbers (afm

    :param afm: Greek Vat Number (9 digits)
    :return: True / False
    """
    afm = str(afm)
    if len(afm) != 9 or not afm.isdigit():
        return False
    tot = sum([(int(afm[i]) * (2 ** (8 - i))) for i in range(8)])
    check = (tot % 11) % 10
    return check == int(afm[8])


def is_amka(amka):
    """Algorithmic check of Greek Social Security Number (AMKA

    :param amka: Greek Social security number (11 digits)
    :return: True / False
    """
    amka = str(amka)
    if len(amka) != 11 or not amka.isdigit():
        return False
    else:
        amkai = [int(i) for i in amka]
        total = amkai[10]
        for i, digit in enumerate(amkai[:10]):
            if (i % 2) != 0:
                total += sum([int(i) for i in str(digit * 2)])
            else:
                total += digit
        return (total % 10) == 0


def is_greek_date(strdate):
    if not type(strdate) == str:
        return False
    if strdate.count('/') != 2:
        return False
    day, month, year = strdate.split('/')
    try:
        day, month, year = int(day), int(month), int(year)
    except:
        return False
    try:
        date(year, month, day)
    except:
        return False
    return True


def is_iso_date(strdate):
    if not type(strdate) == str:
        return False
    if len(strdate) != 10:
        return False
    if strdate.count('-') != 2:
        return False
    year, month, day = strdate.split('-')
    try:
        day, month, year = int(day), int(month), int(year)
    except:
        return False
    try:
        date(year, month, day)
    except:
        return False
    return True


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
