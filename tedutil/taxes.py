"""Various functions for tax purposes"""
from decimal import Decimal
from tedutil.dec import dec
from tedutil.dec import klimaka
from tedutil.grdate import today

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
    2010: (
        (12000, 4000, 6000, 4000, 6000, 8000, 20000, 40000),
        (0, 18, 24, 26, 32, 36, 38, 40, 45),
    ),
    2011: (
        (5000, 7000, 4000, 10000, 14000, 20000, 40000),
        (0, 10, 18, 25, 35, 38, 40, 45),
    ),
    2012: (
        (5000, 7000, 4000, 10000, 14000, 20000, 40000),
        (0, 10, 18, 25, 35, 38, 40, 45),
    ),
    2013: ((25000, 17000), (22, 32, 42)),
    2014: ((25000, 17000), (22, 32, 42)),
    2015: ((25000, 17000), (22, 32, 42)),
    2016: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2017: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2018: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2019: ((20000, 10000, 10000), (22, 29, 37, 45)),
    2020: ((10000, 10000, 10000, 10000), (9, 22, 28, 36, 44)),
    2021: ((10000, 10000, 10000, 10000), (9, 22, 28, 36, 44)),
}

MEI = {
    2017: ((0, 1, 2, 3), (1900, 1950, 2000, 2100)),
    2018: ((0, 1, 2, 3), (1900, 1950, 2000, 2100)),
    2019: ((0, 1, 2, 3), (1900, 1950, 2000, 2100)),
    2020: ((0, 1, 2, 3, 4, 5), (777, 810, 900, 1120, 1340, 1560)),
    2021: ((0, 1, 2, 3, 4, 5), (777, 810, 900, 1120, 1340, 1560)),
}

EEA = {
    2018: ((12000, 8000, 10000, 10000, 25000, 155000), (0, 2.2, 5, 6.5, 7.5, 9, 10)),
    2019: ((12000, 8000, 10000, 10000, 25000, 155000), (0, 2.2, 5, 6.5, 7.5, 9, 10)),
    2020: ((12000, 8000, 10000, 10000, 25000, 155000), (0, 2.2, 5, 6.5, 7.5, 9, 10)),
    2021: ((12000, 8000, 10000, 10000, 25000, 155000), (0, 2.2, 5, 6.5, 7.5, 9, 10)),
}


def foros_etoys(year, yearly_income):
    """Calculates annual tax

    :param year: year
    :param yearly_income: yearly income
    :return: yearly tax
    """
    year = int(year)
    if year not in KLI.keys():
        raise ValueError("Year is out of scope")
    scale, percent = KLI[year]
    return klimaka(yearly_income, scale, percent)


def meiosi_foroy(year, yearly_income, children) -> Decimal:
    """Annual tax reduction

    :param year: year
    :param yearly_income: yearly income
    :param children: Number of children
    :return: reduction
    """
    children = int(children)  # For calculator module compatibility
    paidia, meiosi = MEI.get(year, ((0,), (0,)))
    if children in paidia:
        total_meiosi = meiosi[children]
    else:
        total_meiosi = meiosi[-1]
    over20k = yearly_income - 20000
    if over20k <= 0:
        return dec(total_meiosi)
    times, rest = over20k // 1000, over20k % 1000
    rest = 1 if rest > 0 else 0
    final_meiosi = total_meiosi - (times + rest) * 10
    if final_meiosi > 0:
        return dec(final_meiosi)
    return dec(0)


def foros_etoys_me_ekptosi(year, yearly_income, children=0) -> Decimal:
    """Calculates annual tax with reduction

    :param year: year
    :param yearly_income: yearly income
    :param children: Number of children
    :return: annual tax payable
    """
    foros = foros_etoys(year, yearly_income)
    meion = meiosi_foroy(year, yearly_income, children)
    final = foros - meion
    return final if final > 0 else dec(0)


def foros_periodoy(year, apodoxes, children=0, barytis=14, extra=0) -> Decimal:
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
    return dec(foros / dec(barytis) + delta)


def eea_etoys(year, yearly_income):
    """Calculates special tax

    :param year: year
    :param yearly_income: yearly income
    :return: special tax payable
    """
    if year not in EEA.keys():
        return dec(0)
    scale, percent = EEA[year]
    return klimaka(yearly_income, scale, percent)


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
    return dec(eea / dec(barytis) + delta)


def foros_eea_periodoy(year, apodoxes, barytis=14, paidia=0, extra=0):
    """Calculates tax and special tax together for given period

    :param year: year
    :param apodoxes: period income
    :param barytis: period slice
    :param paidia: number of children
    :param extra: extra income (current period only)
    :return: dictionary of tax, special tax, payable
    """
    year = int(year)
    foros = foros_periodoy(year, apodoxes, paidia, barytis, extra)
    eea = eea_periodoy(year, apodoxes, barytis, extra)
    apod = dec(apodoxes + extra)
    kath = apod - foros - eea
    return {"foros": foros, "eea": eea, "forolog": apod, "pliroteo": kath}


def reverse_apodoxes(year, katharo, pikaerg, paidia=0):
    """Να βρούμε από τα καθαρά τα μικτά

    :param year:
    :param katharo:
    :param pikaerg:
    :param paidia:
    :return:
    """
    katharo = dec(katharo)
    synt1 = dec(1 - dec(pikaerg) / dec(100), 4)
    mikto = dec(katharo / synt1)
    apot = foros_eea_periodoy(year, katharo)

    delta = katharo - apot["pliroteo"]
    # print(pros1, delta, apot)
    i = 0
    while delta > 0 and i < 100:
        i += 1
        mikto += delta
        ap2 = foros_eea_periodoy(year, mikto * synt1, paidia=paidia)
        delta = katharo - ap2["pliroteo"]
    return mikto


def mikta_apo_kathara(katharo, pika, paidia=0, period=None):
    if period is None:
        period = today("%Y%m")
    period = str(period)
    year = period[:4]
    return reverse_apodoxes(year, katharo, pika, paidia)


def test_apodoxes(year, mikto, pikaerg, paidia=0):
    mikto = dec(mikto)
    krika = dec(mikto * dec(pikaerg, 4) / dec(100))
    forol = mikto - krika
    result = foros_eea_periodoy(year, forol, paidia=paidia)
    result["paidia"] = paidia
    result["mikto"] = mikto
    result["pika"] = "%s%%" % pikaerg
    result["ika"] = krika
    result["krat"] = result["foros"] + result["eea"] + result["ika"]
    return result


def kostos_misthodosias(misthos, pikaergodoti):
    analogia_doroy = misthos / 8 * 12.5 / 12
    analogia_epidomatos = misthos / 24
    analogia_adeias = misthos * 2 / 25
    mikta = misthos + analogia_doroy + analogia_epidomatos + analogia_adeias
    ika_ergodoti = mikta * pikaergodoti / 100
    total = mikta + ika_ergodoti
    return total


def foros2020(income, children=0):
    income = dec(income)
    kli, pos = (10000, 10000, 10000, 10000), (9, 22, 28, 36, 44)
    foros_xoris_meiosi = klimaka(income, kli, pos)
    # Μείωση φόρου
    klimaka_meiosis = (777, 810, 900)
    if children <= 2:
        meiosi_total = klimaka_meiosis[children]
    else:
        meiosi_total = klimaka_meiosis[2] + 220 * (children - 2)
    meiosi_meiosis = 0
    if children < 5 and income > 12000:
        meiosi_meiosis = (income - 12000) // 1000 * 20
    if meiosi_meiosis > meiosi_total:
        meiosi_meiosis = meiosi_total
    meiosi = meiosi_total - meiosi_meiosis
    if meiosi > foros_xoris_meiosi:
        meiosi = foros_xoris_meiosi
    # Φόρος χρήσης
    foros = foros_xoris_meiosi - meiosi
    # Ειδικό επίδομα αλληλεγγύης
    eea_kli = (12000, 8000, 10000, 10000, 25000, 155000)
    eea_pos = (0, 2.2, 5, 6.5, 7.5, 9, 10)
    eea = klimaka(income, eea_kli, eea_pos)
    return {
        "income": income,
        "children": children,
        "foros-xoris-ekptosi": foros_xoris_meiosi,
        "ekptosi-klimakas": meiosi_total,
        "meiosi-ekptosis": meiosi_meiosis,
        "ekptosi-teliki": meiosi,
        "foros": foros,
        "eea": eea,
        "foros-eea": foros + eea,
        "pososto": round((foros + eea) / income * dec(100), 2),
        "pliroteo": income - foros - eea,
    }


def foros(etos, income, children=0):
    forosd = {2020: foros2020, 2021: foros2020}
    ietos = int(etos)
    if ietos in forosd:
        return forosd[ietos](income, children)
    raise ValueError(f"Δεν υπάρχει υπολογισμός για το έτος {etos}")
