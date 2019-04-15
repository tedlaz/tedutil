"""Generators for Greek amka/afm for testing purposes"""
from random import randint
from random import choice
from random import choices
from datetime import datetime
from tedutil.amka import is_amka
from tedutil.afm import is_afm
file_eponyma = "/home/ted/Documents/grnames/eponyma.csv"
file_females = "/home/ted/Documents/grnames/sfemale.csv"
file_males = "/home/ted/Documents/grnames/smale.csv"


def load_names(dfile):
    names = []
    frequency = []
    with open(dfile, encoding="utf8") as fil:
        for lin in fil:
            if len(lin) < 3:
                continue
            name, freq, *_ = lin.strip().split(';')
            names.append(name)
            frequency.append(int(freq))
    return names, frequency


def load_surnames(dfile):
    smnames = []
    sfnames = []
    with open(dfile, encoding="utf8") as fil:
        for lin in fil:
            if len(lin) < 3:
                continue
            sna = lin.split()
            if len(sna) == 1:
                smnames.append(sna[0])
                sfnames.append(sna[0])
            else:
                smnames.append(sna[0])
                sfnames.append(sna[1])
    return smnames, sfnames


def distribution(alist, center, density=1):
    try:
        index_center = alist.index(center)
    except ValueError:
        index_center = len(alist) // 2
    # print(index_center)
    left = alist[:index_center]
    right = alist[index_center+1:]
    len_left = len(left)
    len_right = len(right)
    mxl = max(len_left, len_right)
    # print(left, right, mxl)
    stleft = [i+1 for i in range(mxl)][mxl-len_left:]
    rmxl = list(range(mxl))
    rmxl.reverse()
    # print(rmxl)
    stright = [i+1 for i in rmxl][:len_right]
    stleft.append(mxl+1)
    final = stleft + stright
    return [i**density for i in final]


def distribution_range(apo, eos, center=None, density=3):
    points = list(range(apo, eos + 1))
    return points, distribution(points, center, density)


def generate_amka(year=None):
    """Greek social security number (amka) generator

    :return: algorithmically valid amka
    """
    mon = str(randint(101, 112))[1:]
    day = str(randint(101, 128))[1:]
    if year:
        yea = year
    else:
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


def generate_all(number, age_apo=18, age_eos=65, center=None, density=3):
    year_now = datetime.now().year
    points, dist = distribution_range(age_apo, age_eos, center, density)
    # print(dist)
    years = [str(abs(i - year_now))[2:] for i in points]
    males, freq_males = load_names(file_males)
    females, freq_females = load_names(file_females)
    sur_males, sur_females = load_surnames(file_eponyma)
    for _ in range(number):
        mf = randint(0, 1)
        if mf == 0:
            nam = choices(males, freq_males)[0].capitalize()
            snam = choice(sur_males).capitalize()
        else:
            nam = choices(females, freq_females)[0].capitalize()
            snam = choice(sur_females).capitalize()
        father = choices(males, freq_males)[0].capitalize()
        mother = choices(females, freq_females)[0].capitalize()
        amka = generate_amka(choices(years, dist)[0])
        afm = generate_afm()
        while mother == nam:  # όχι ιδιο μητρώνυμο και όνομα
            mother = choices(females, freq_females)[0].capitalize()
        while father == nam:  # όχι ίδιο πατρώνυμο και όνομα
            father = choices(males, freq_males)[0].capitalize()
        epoon = "%s %s" % (snam, nam)
        print("%-40s %-20s %-20s %s %s" % (epoon, father, mother, amka, afm))


if __name__ == "__main__":
    generate_all(10, 25, 60, center=35, density=3)
    # print(distribution(18, 29))
    # print(distribution(18, 29, 21))
    # print(generate_year(18, 28, 2019, 2))
