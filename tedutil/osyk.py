"""




        Γίνονται κλήσεις στο αρχείο πολλαπλές χωρίς λόγο

        Πρέπει να γίνει διόρθωση ...



"""
import os
from functools import lru_cache
from tedutil import files as fls
from tedutil import grtext as grt
URLF = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"


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
        leid, lper, *_ = grt.split_strip(lin)
        if str(eid) == leid:
            return leid, lper
    return None


def kad_find(kad, fname='dn_kad.txt', osyk=None):
    """Εύρεση εγγραφής ΚΑΔ με βάση τον κωδικό

    input parameters
      kad=Αριθμός ΚΑΔ(Κωδικός αριθμός δραστηριότητας)

    returns
      tuple (ΚΑΔ, Περιγραφή ΚΑΔ)

    Finds and returns record with given no
    """
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
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
    kads = []
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


def eid_kad_list(kad, per, fname='dn_kadeidkpk.txt', osyk=None):
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
    per = int(per)  # Make sure per is integer for comparison
    arr = []
    chck = {}
    i = 0
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
        if len(lin) < 10:
            continue
        lkad, eid, kpk, apo, eos, *_ = grt.split_strip(lin)
        ckv = '%s%s' % (lkad, eid)
        if skad == lkad and (int(eos) >= per >= int(apo)) and ckv not in chck:
            _, eidp = eid_find(eid, osyk=osyk)
            arr.append([lkad, eid, kpk, apo, eos, eidp])
            chck[ckv] = i
            i = i + 1
    return arr


def eid_kad_string(kad, period):
    """Print eids"""
    tmpl = '%6s %3s %s\n'
    tsr = 'Ειδικότητες εργασίας για τον %s την περίοδο %s\n' % (kad, period)
    for eid in eid_kad_list(kad, period):
        tsr += tmpl % (eid[1], eid[2], eid[5])
    return tsr


@lru_cache()
def kpk_find(kpk, per, fname='dn_kpk.txt', osyk=None):
    """
    input parameters
      kpk=Κωδ.Πακέτου κάλυψης, per=Περίοδος(YYYMM)

    returns
      tuple (ΚΠΚ, Περιγραφή, Εργ%, Εργοδότης%, Σύνολο%, περίοδος ισχύος)
    """
    per = int(per)
    for lin in fls.zipfile_data(get_osyk(osyk), fname):
        if len(lin) < 15:
            continue
        lkp, nam, ikaer, ikaetis, ikat, lper, *_ = grt.split_strip(lin)
        if str(kpk) == lkp:
            if per >= int(lper):
                return lkp, nam, ikaer, ikaetis, ikat, lper
    return None


def kadeidkpk_find(kad, eid, per, file_name='dn_kadeidkpk.txt', osyk=None):
    """
    input parameters
      kad=Κωδ.Αρ.Δραστ, eid=Ειδικότητα, per=Περίοδος

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος, ΚΠΚ, tuple(kpk_find))
    """
    kad = str(kad)
    eid = str(eid)
    per = int(per)
    for lin in fls.zipfile_data(get_osyk(osyk), file_name):
        if len(lin) < 10:
            continue
        lka, lei, lkp, apo, eos, *_ = grt.split_strip(lin)
        if kad == lka and eid == lei:
            if int(eos) >= per >= int(apo):
                return kad, eid, per, lkp, kpk_find(lkp, per, osyk=osyk)
    return None
