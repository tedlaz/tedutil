"""Greek date functions"""


def iso2gr(date):
    """Transform iso date string to greek formatted date string

    :param date: Iso formatted date string (yyyy-mm-dd)
    :return: Greek formatted date string (dd/mm/yyyy)
    """
    strdate = str(date)
    try:
        year, month, day = strdate.split('-')
        return '%s/%s/%s' % (day, month, year)
    except ValueError:
        return '01/01/1000'


def gr2iso(grdate):
    """Transform Greek date string to iso date string

    :param grdate: Greek Date string
    :return: Iso Date string
    """
    strdate = str(grdate)
    try:
        day, month, year = strdate.split('/')
    except ValueError:
        return '1000-01-01'
    if len(month) > 2 or len(day) > 2 or len(year) != 4:
        return '1000-01-01'
    day = day if len(day) == 2 else '0' + day
    month = month if len(month) == 2 else '0' + month
    return '%s-%s-%s' % (year, month, day)


def date2period_end(isodate):
    """Transform iso date to last trimino date

    :param isodate:
    :return: YYYY-MM-LAST-DATE-OF-3MONTH
    """
    year, month, _ = isodate.split('-')
    imonth = int(month)
    if imonth <= 3:
        return '%s-%s-%s' % (year, '03', '31')
    elif imonth <= 6:
        return '%s-%s-%s' % (year, '06', '30')
    elif imonth <= 9:
        return '%s-%s-%s' % (year, '09', '30')
    elif imonth <= 12:
        return '%s-%s-%s' % (year, '12', '31')
    else:
        return '%s-%s-%s' % (year, '12', '31')


def date2per(isodate, rate=2):
    """Returns Year-Period Type-Period Number

    :param isodate:
    :param rate:
    :return:
    """
    stt = "%s%s%s"
    year, month, _ = isodate.split('-')
    if rate not in (1, 2, 3, 4, 6):
        return stt % (year, 1, 1)
    imonth = int(month)
    per = imonth // rate
    rem = imonth % rate
    if rem > 0:
        per += 1
    return stt % (year, rate, per)


def season(isodate, startmonth=10):
    """Iso date to Season (YearFrom-YearTo)

    :param isodate:
    :param startmonth:
    :return: (YYYY-YYYY)
    """
    year, month, day = isodate.split('-')
    if int(month) >= startmonth:
        return '%s-%s' % (year, int(year) + 1)
    else:
        return '%s-%s' % (int(year) - 1, year)
