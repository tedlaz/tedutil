def check_validity(chart, eelines):
    """Έλεγχος εάν όλοι οι λογαριασμοί που πρέπει να μπουν στο
	   Βιβλίο εσόδων-Εξόδων έχουν σωστή παράμετρο

     [ee]
     # ee    perigrafi
		 2.24    Αγορές ΦΠΑ 24%

		 [acc]
	   # Λμός        Λ/μος ΦΠΑ     NR  CH  Φ2       ΕΕ
     20.01.00.024  54.00.20.024  24  24  361      2.24

     Θα πρέπει η τιμή ΕΕ(2.24) του [acc] να υπάρχει στο [ee]
    """
    for val in chart.values():
        if val['ee'] == '':
            continue
        if val['ee'] not in eelines:
            raise ValueError(f"{val['ee']} not in {eelines}")


def acc_parse(fil):
    """Εδώ παρσάρουμε το αρχείο με τις παραμέτρους των :
       1. Στηλών βιβλίου Εσόδων-Εξόδων
       2. Κινούμενων λογαριασμών λογιστικής
       3. Λογιστικού σχεδίου ανωτεροβαθμίων μή κινούμενων
    """
    chart = {}
    ee_lines = {}
    chart0 = {}
    state = 0
    with open(fil) as ofl:
        for line in ofl.readlines():
            sline = line.strip()
            if len(sline) < 3:
                continue
            if sline.startswith('#'):
                continue
            if sline == "[acc]":
                state = 1
                continue
            elif sline == "[ee]":
                state = 2
                continue
            elif sline == "[chart]":
                state = 3
                continue

            if state == 1:
                try:
                    # Λμός Λ/μος ΦΠΑ     NR  CH  Φ2       ΕΕ
                    acc, vacc, nr, ch, f2, ee = sline.split()
                    vacc = '' if vacc == '-' else vacc
                    nr = 0 if nr == '-' else int(nr)
                    ch = 0 if ch == '-' else int(ch)
                    f2 = '' if f2 == '-' else f2
                    ee = '' if ee == '-' else ee
                    chart[acc] = {'acc': acc, 'vacc': vacc, 'nr': nr, 'ch': ch, 'f2': f2, 'ee': ee}
                except Exception:
                    continue
            elif state == 2:
                try:
                    ee, *per = sline.split()
                    ee_lines[ee] = ' '.join(per)
                except Exception:
                    continue

            elif state == 3:
                try:
                    pass
                    acc, *per = sline.split()
                    chart0[acc] = ' '.join(per)
                except Exception:
                    continue

    check_validity(chart, ee_lines)
    return chart, chart0, ee_lines


def match_account(acc, chart):
    """Ας πούμε ότι ο λογαριασμός είναι ο 65.00.00.000
       εμείς θα πρέπει να βρούμε την γραμμή από το chart του 65

    """
    for i in range(len(acc) + 1)[::-1]:
        if acc[:i] in chart:
            return chart[acc[:i]]
    raise ValueError(f"{acc} not in given chart")
