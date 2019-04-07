"""Generators for Greek amka/afm for testing purposes"""
from random import randint
from tedutil.amka import is_amka
from tedutil.afm import is_afm


def generate_amka():
    """Greek social security number (amka) generator

    :return: algorithmically valid amka
    """
    mon = str(randint(101, 112))[1:]
    day = str(randint(101, 128))[1:]
    yea = str(randint(100, 199))[1:]
    res = str(randint(10000, 10999))[1:]
    for i in range(10):
        num = '%s%s%s%s%s' % (day, mon, yea, res, i)
        if is_amka(num):
            return num


def generate_afm():
    """Greek tax number (afm) generator

    :return: algorithmically valid afm
    """
    no1 = str(randint(100000000, 999999999))[1:]
    for i in range(10):
        num = '%s%s' % (no1, i)
        if is_afm(num):
            return num


if __name__ == "__main__":
    print(generate_amka())
    print(generate_afm())
