def iso2gr(date):
    """

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
    """

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
    return '%s-%s-%s' % (year, month, day )
