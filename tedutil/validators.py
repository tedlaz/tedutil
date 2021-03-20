"""Greek VAT and Social Security Number validation functions"""


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
