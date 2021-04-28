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


class F2Ee:
    def __init__(self):
        self.acount = '24.01.00.024'
        self.fpa_account = '54.00.24.024'
        self.fpa4f2 = 24
        self.fpa4check = 24
        self.f2_codes = ['361']
        self.ee_code = '2.e'

    def check_transaction(self, tran):
        for lin in tran.lines:
            pass


def acc_parse(fil):
    """Εδώ παρσάρουμε το αρχείο με τις παραμέτρους των :
       1. Στηλών βιβλίου Εσόδων-Εξόδων
       2. Κινούμενων λογαριασμών λογιστικής
       3. Λογιστικού σχεδίου ανωτεροβαθμίων μή κινούμενων
    """
    f2ee = {}
    ee_lines = {}
    chart0 = {}
    F2EE, EE_LINES, CHART0 = 1, 2, 3
    state = 0
    with open(fil) as ofl:
        for line in ofl.readlines():
            sline = line.strip()
            if len(sline) < 3:
                continue
            if sline.startswith('#'):
                continue
            if sline == "[f2ee]":
                state = F2EE
                continue
            elif sline == "[ee_lines]":
                state = EE_LINES
                continue
            elif sline == "[chart0]":
                state = CHART0
                continue

            if state == F2EE:
                # Λμός Λ/μος ΦΠΑ     NR  CH  Φ2       ΕΕ
                acc, vacc, nr, ch, f2, ee = sline.split()
                vacc = '' if vacc == '-' else vacc
                nr = 0 if nr == '-' else int(nr)
                ch = 0 if ch == '-' else int(ch)
                f2 = '' if f2 == '-' else f2
                ee = '' if ee == '-' else ee
                f2ee[acc] = {
                    'account': acc,
                    'fpa-account': vacc,
                    'f2-fpa': nr,
                    'check-fpa': ch,
                    'f2-codes': f2.split('|'),
                    'ee': ee
                }

            elif state == EE_LINES:
                ee, *per = sline.split()
                ee_lines[ee] = ' '.join(per)

            elif state == CHART0:
                acc, *per = sline.split()
                chart0[acc] = ' '.join(per)

    check_validity(f2ee, ee_lines)
    return f2ee, chart0, ee_lines


def match_account(acc, chart):
    """Ας πούμε ότι ο λογαριασμός είναι ο 65.00.00.000
       εμείς θα πρέπει να βρούμε την γραμμή από το chart του 65

    """
    for i in range(len(acc) + 1)[::-1]:
        if acc[:i] in chart:
            return chart[acc[:i]]
    raise ValueError(f"{acc} not in given chart")
