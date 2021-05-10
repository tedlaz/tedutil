"""Greek date functions"""
import datetime

MONTHGR = [
    "Ιανουάριος",
    "Φεβρουάριος",
    "Μάρτιος",
    "Απρίλιος",
    "Μάϊος",
    "Ιούνιος",
    "Ιούλιος",
    "Αύγουστος",
    "Σεπτέμβριος",
    "Οκτώβριος",
    "Νοέμβριος",
    "Δεκέμβριος",
]
MONTHPGR = [
    "Ιανουαρίου",
    "Φεβρουαρίου",
    "Μαρτίου",
    "Απριλίου",
    "Μαΐου",
    "Ιουνίου",
    "Ιουλίου",
    "Αυγούστου",
    "Σεπτεμβρίου",
    "Οκτωβρίου",
    "Νοεμβρίου",
    "Δεκεμβρίου",
]
DAYGR = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
DAYPGR = [
    "Δευτέρας",
    "Τρίτης",
    "Τετάρτης",
    "Πέμπτης",
    "Παρασκευής",
    "Σαββάτου",
    "Κυριακής",
]


def iso2gr(date: str) -> str:
    """Transform iso date string to greek formatted date string

    :param date: Iso formatted date string (yyyy-mm-dd)
    :return: Greek formatted date string (dd/mm/yyyy)
    """
    strdate = str(date)
    try:
        year, month, day = strdate.split("-")
        return "%s/%s/%s" % (day, month, year)
    except ValueError:
        return "01/01/1000"


def gr2iso(grdate: str) -> str:
    """Transform Greek date string to iso date string

    :param grdate: Greek Date string
    :return: Iso Date string
    """
    strdate = str(grdate)
    try:
        day, month, year = strdate.split("/")
    except ValueError:
        return "1000-01-01"
    if len(month) > 2 or len(day) > 2 or len(year) != 4:
        return "1000-01-01"
    day = day if len(day) == 2 else "0" + day
    month = month if len(month) == 2 else "0" + month
    return "%s-%s-%s" % (year, month, day)


def date2period_end(isodate: str) -> str:
    """Transform iso date to last trimino date

    :param isodate:
    :return: YYYY-MM-LAST-DATE-OF-3MONTH
    """
    year, month, _ = isodate.split("-")
    imonth = int(month)
    if imonth <= 3:
        return "%s-%s-%s" % (year, "03", "31")
    elif imonth <= 6:
        return "%s-%s-%s" % (year, "06", "30")
    elif imonth <= 9:
        return "%s-%s-%s" % (year, "09", "30")
    elif imonth <= 12:
        return "%s-%s-%s" % (year, "12", "31")
    else:
        return "%s-%s-%s" % (year, "12", "31")


def date2per(isodate: str, rate=2) -> str:
    """Returns Year-Period Type-Period Number

    :param isodate:
    :param rate:
    :return:
    """
    stt = "%s%s%s"
    year, month, _ = isodate.split("-")
    if rate not in (1, 2, 3, 4, 6):
        return stt % (year, 1, 1)
    imonth = int(month)
    per = imonth // rate
    rem = imonth % rate
    if rem > 0:
        per += 1
    return stt % (year, rate, per)


def season(isodate: str, startmonth=10) -> str:
    """Iso date to Season (YearFrom-YearTo)

    :param isodate:
    :param startmonth:
    :return: (YYYY-YYYY)
    """
    year, month, _ = isodate.split("-")
    if int(month) >= startmonth:
        return "%s-%s" % (year, int(year) + 1)
    else:
        return "%s-%s" % (int(year) - 1, year)


def today(format_string: str = "%Y%m%d") -> str:
    """Today's date in different formats

    :param format_string: "%Y%m%d","%Y-%m-%d","%d/%m/%Y" ,"%Y-%m-%d %H:%M:%S"
    :return: current date as string
    """
    return datetime.datetime.now().strftime(format_string)


def current_period(format_string: str = "%Y%m") -> str:
    """Today's date in different formats

    :param format_string: "%Y%m%d","%Y-%m-%d","%d/%m/%Y" ,"%Y-%m-%d %H:%M:%S"
    :return: current date as string
    """
    return datetime.datetime.now().strftime(format_string)


def date_in_interval(date, date_from=None, date_to=None) -> bool:
    if date_from and date_from > date:
        return False
    if date_to and date_to < date:
        return False
    return True
