"""Various functions for tax purposes"""


from . import dec
# Πριν το 2002 το νόμισμα ήταν η δραχμή
KLI = {
    2002: ((7400, 1000, 5000, 10000), (0, 5, 15, 30, 40)),
    2003: ((11000, 3400, 10000), (0, 15, 30, 40)),
    2004: ((10000, 3400, 10000), (0, 15, 30, 40)),
    2005: ((11000, 2000, 10000), (0, 15, 30, 40)),
    2006: ((11000, 2000, 10000), (0, 15, 30, 40)),
    2007: ((12000, 18000, 45000), (0, 27, 39, 40)),
    2008: ((12000, 18000, 45000), (0, 27, 37, 40)),
    2009: ((12000, 18000, 45000), (0, 25, 35, 40)),
    2010: ((12000, 4000, 6000, 4000, 6000, 8000, 20000, 40000),
           (0, 18, 24, 26, 32, 36, 38, 40, 45)),
    2011: ((5000, 7000, 4000, 10000, 14000, 20000, 40000),
           (0, 10, 18, 25, 35, 38, 40, 45)),
    2012: ((5000, 7000, 4000, 10000, 14000, 20000, 40000),
           (0, 10, 18, 25, 35, 38, 40, 45)),
    2013: ((25000, 17000), (22, 32, 42)),
    2014: ((25000, 17000), (22, 32, 42)),
    2015: ((25000, 17000), (22, 32, 42)),
    2016: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2017: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2018: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2019: ((20000, 10000, 10000), (22, 29, 37, 45)),
}

MEI = {
    2017: ((0, 1, 2, 3), (1900, 1950, 2000, 2100)),
    2018: ((0, 1, 2, 3), (1900, 1950, 2000, 2100)),
    2019: ((0, 1, 2, 3), (1900, 1950, 2000, 2100))
}

EEA = {
    2018: ((12000, 8000, 10000, 10000, 25000, 155000),
           (0, 2.2, 5, 6.5, 7.5, 9, 10)),
    2019: ((12000, 8000, 10000, 10000, 25000, 155000),
           (0, 2.2, 5, 6.5, 7.5, 9, 10)),
}


def foros_etoys(year, yearly_income):
    """Calculates annual tax

    :param year: year
    :param yearly_income: yearly income
    :return: yearly tax
    """
    if year not in KLI.keys():
        raise ValueError("Year is out of scope")
    scale, percent = KLI[year]
    return dec.klimaka(yearly_income, scale, percent)


def meiosi_foroy(year, yearly_income, children):
    """Annual tax reduction

    :param year: year
    :param yearly_income: yearly income
    :param children: Number of children
    :return: reduction
    """
    paidia, meiosi = MEI.get(year, ((0,), (0,)))
    if children in paidia:
        total_meiosi = meiosi[children]
    else:
        total_meiosi = meiosi[-1]
    over20k = yearly_income - 20000
    if over20k <= 0:
        return dec.dec(total_meiosi)
    times, rest = over20k // 1000, over20k % 1000
    rest = 1 if rest > 0 else 0
    final_meiosi = total_meiosi - (times + rest) * 10
    if final_meiosi > 0:
        return dec.dec(final_meiosi)
    return dec.dec(0)


def foros_etoys_me_ekptosi(year, yearly_income, children=0):
    """Calculates annual tax with reduction

    :param year: year
    :param yearly_income: yearly income
    :param children: Number of children
    :return: annual tax payable
    """
    foros = foros_etoys(year, yearly_income)
    meion = meiosi_foroy(year, yearly_income, children)
    final = foros - meion
    return final if final > 0 else dec.dec(0)


def foros_periodoy(year, apodoxes, children=0, barytis=14, extra=0):
    """Calculates tax for period

    :param year: year
    :param apodoxes: period income
    :param children: number of children
    :param barytis: period slice
    :param extra: extra income (current period only)
    :return: period tax payable
    """
    yearly = apodoxes * barytis
    tyearly = (apodoxes * barytis) + extra
    tforos = foros_etoys_me_ekptosi(year, tyearly, children)
    foros = foros_etoys_me_ekptosi(year, yearly, children)
    delta = tforos - foros
    return dec.dec(foros / dec.dec(barytis) + delta)


def eea_etoys(year, yearly_income):
    """Calculates special tax

    :param year: year
    :param yearly_income: yearly income
    :return: special tax payable
    """
    if year not in EEA.keys():
        return dec.dec(0)
    scale, percent = EEA[year]
    return dec.klimaka(yearly_income, scale, percent)


def eea_periodoy(year, apodoxes, barytis=14, extra=0):
    """Calculates special tax for period

    :param year: year
    :param apodoxes: period income
    :param barytis: period slice
    :param extra: extra income (current period only)
    :return: special tax for period payable
    """
    yearly = apodoxes * barytis
    tyearly = (apodoxes * barytis) + extra
    teea = eea_etoys(year, tyearly)
    eea = eea_etoys(year, yearly)
    delta = teea - eea
    return dec.dec(eea / dec.dec(barytis) + delta)


def foros_eea_periodoy(year, apodoxes, barytis=14, paidia=0, extra=0):
    """Calculates tax and special tax together for given period

    :param year: year
    :param apodoxes: period income
    :param barytis: period slice
    :param paidia: number of children
    :param extra: extra income (current period only)
    :return: dictionary of tax, special tax, payable
    """
    foros = foros_periodoy(year, apodoxes, paidia, barytis, extra)
    eea = eea_periodoy(year, apodoxes, barytis, extra)
    apod = dec.dec(apodoxes + extra)
    kath = apod - foros - eea
    return {'foros': foros, 'eea': eea, 'apodoxes': apod, 'pliroteo': kath}
