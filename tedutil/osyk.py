"""




        Γίνονται κλήσεις στο αρχείο πολλαπλές χωρίς λόγο

        Πρέπει να γίνει διόρθωση ...



"""
import os
from functools import lru_cache
from tedutil import files as fls
from tedutil import grtext as grt
from tedutil.grdate import current_period
URLF = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"


@lru_cache()
def get_osyk(file_path=None):
    if file_path is None:
        return fls.download_file(URLF, os.getcwd())
    else:
        return file_path


def eid_find(eid, fname='dn_eid.txt', osyk=None):
    """Εύρεση ειδικότητας με βάση τον κωδικό

    input parameters
      eid=Κωδικός Ειδικότητας

    returns
      tuple (Κωδικός ειδικότητας, περιγραφή ειδικότητας)
    """
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
        if len(lin) < 3:
            continue
        leid, lper, *_ = grt.split_strip(lin)
        if str(eid) == leid:
            return leid, lper
    return None


def eid_find_by_name(eidper, fname='dn_eid.txt', osyk=None):
    """Εύρεση ειδικότητας με βάση τον κωδικό

    input parameters
      eid=Κωδικός Ειδικότητας

    returns
      tuple (Κωδικός ειδικότητας, περιγραφή ειδικότητας)
    """
    found = list()
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
        if len(lin) < 3:
            continue
        leid, lper, *_ = grt.split_strip(lin)
        if grt.grup(str(eidper)) in grt.grup(lper):
            found.append([leid, lper])
    return found if found else None


def kad_find(kad, fname='dn_kad.txt', osyk=None):
    """Εύρεση εγγραφής ΚΑΔ με βάση τον κωδικό

    input parameters
      kad=Αριθμός ΚΑΔ(Κωδικός αριθμός δραστηριότητας)

    returns
      tuple (ΚΑΔ, Περιγραφή ΚΑΔ)

    Finds and returns record with given no
    """
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
        if len(lin) < 5:
            continue
        lkad, lper, *_ = grt.split_strip(lin)
        if str(kad) == lkad:
            return lkad, lper
    return None


def kad_list(kadno='', fname='dn_kad.txt', osyk=None):
    """
    input parameters
      kad=Κωδικός Αριθμός δραστηριότητας

    returns
      List [[kad1, kadper1], [kad2, kadper2], ..]
    """
    kadno = str(kadno)
    kads = list()
    for line in fls.zipfile_data(get_osyk(osyk), fname):
        if len(line) < 6:
            continue
        lkad, lper, *_ = grt.split_strip(line)
        if kadno == '':
            kads.append((lkad, lper))
        else:
            if lkad.startswith(kadno):
                kads.append((lkad, lper))
    return kads


def eid_kad_list(kad, period=None, filename='dn_kadeidkpk.txt', osyk=None):
    """
    input parameters
      kad=Κωδ.Αρ.Δραστηριότητας, per=Περίοδος(YYYYMM) πχ 201301

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος από, ΚΠΚ, Περίοδος έως, Περιγρ.Ειδικότητας)

    Σχόλια
    Τα αρχεία του ΙΚΑ δεν είναι σε μερικές περιπτώσεις κανονικοποιημένα
    με αποτέλεσμα να υπάρχουν για ΚΑΔ, ΕΙΔ, περίοδο διπλές εγγραφές.
    Λύση προς το παρόν είναι η επιλογή μόνο της πρώτης εγγραφής.
    """
    skad = str(kad)
    period = int(current_period()) if period is None else int(period)
    arr = list()
    chck = dict()
    i = 0
    for lin in fls.zipfile_data(get_osyk(osyk), filename):
        if len(lin) < 10:
            continue
        lkad, eid, kpk, apo, eos, *_ = grt.split_strip(lin)
        ckv = '%s%s' % (lkad, eid)
        iapo, ieos = int(apo), int(eos)
        if skad == lkad and (ieos >= period >= iapo) and ckv not in chck:
            _, eidp = eid_find(eid, osyk=osyk)
            arr.append([lkad, eid, kpk, apo, eos, eidp])
            chck[ckv] = i
            i = i + 1
    return arr


def eid_kad_string(kad, period=None):
    """Print eids"""
    period = int(current_period()) if period is None else int(period)
    tmpl = '%6s %3s %s\n'
    tsr = 'Ειδικότητες εργασίας για τον %s την περίοδο %s\n' % (kad, period)
    for eid in eid_kad_list(kad, period):
        tsr += tmpl % (eid[1], eid[2], eid[5])
    return tsr


@lru_cache()
def kpk_find(kpk, period=None, filename='dn_kpk.txt', osyk=None):
    """
    input parameters
      kpk=Κωδ.Πακέτου κάλυψης, per=Περίοδος(YYYMM)

    returns
      tuple (ΚΠΚ, Περιγραφή, Εργ%, Εργοδότης%, Σύνολο%, περίοδος ισχύος)
    """
    period = int(current_period()) if period is None else int(period)
    for lin in fls.zipfile_data(get_osyk(osyk), filename):
        if len(lin) < 15:
            continue
        lkp, nam, ikaer, ikaetis, ikat, lper, *_ = grt.split_strip(lin)
        if str(kpk) == lkp:
            if period >= int(lper):
                return lkp, nam, ikaer, ikaetis, ikat, lper
    return None


def kadeidkpk_find(kad, eid, period=None, file_name='dn_kadeidkpk.txt',
                   osyk=None):
    """
    input parameters
      kad=Κωδ.Αρ.Δραστ, eid=Ειδικότητα, per=Περίοδος

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος, ΚΠΚ, tuple(kpk_find))
    """
    kad = str(kad)
    eid = str(eid)
    period = int(current_period()) if period is None else int(period)
    for lin in fls.zipfile_data(get_osyk(osyk), file_name):
        if len(lin) < 10:
            continue
        lka, lei, lkp, apo, eos, *_ = grt.split_strip(lin)
        if kad == lka and eid == lei:
            if int(eos) >= period >= int(apo):
                return kad, eid, period, lkp, kpk_find(lkp, period, osyk=osyk)
    return None


def find(value):
    str_value = str(value)
    # int_value = int(value)
    len_value = len(str_value)
    if str_value.isdigit():
        if len_value == 3:
            return kpk_find(value)
        elif len_value == 4:
            return kad_find(value)
        elif len_value == 6:
            return eid_find(value)
    return eid_find_by_name(str_value)
