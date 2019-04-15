"""Για να χρησιμοποιηθεί με την sqlite μισθοδοσία θα πρέπει να υπάρχουν τα
   παρακάτω views :

CREATE VIEW fmy AS
SELECT  m12_xrisi.xrisi, m12_period.id, m12_fpr.afm, m12_fpr.epon, m12_fpr.onom,
        m12_fpr.patr,m12_fpr.amka,0 as paidia,
        sum( case when mtyp_id=200 then val end) as akapod,
        sum( case when mtyp_id=500 then val end) as krat,
        sum( case when mtyp_id=599 then val end) as kaapod,
        sum( case when mtyp_id=600 then val end) as parfor,
        sum( case when mtyp_id=610 then val end) as eea,
        m12_eid.eidp,
        1 as apty
FROM m12_misd
INNER JOIN m12_pro on m12_pro.id = m12_misd.pro_id
INNER JOIN m12_fpr on m12_fpr.id = m12_pro.fpr_id
INNER JOIN m12_mis on m12_mis.id = m12_misd.mis_id
INNER JOIN m12_eid on m12_eid.id = m12_pro.eid_id
INNER JOIN m12_period on m12_period.id=m12_mis.period_id
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
GROUP BY  m12_mis.xrisi_id, m12_period.id, m12_fpr.afm
ORDER BY  m12_mis.xrisi_id, m12_period.id, m12_fpr.epon


CREATE VIEW codata AS
select cop as cepo, 0 as eo, afm as cafm, dra as ant,
       pol as poli, odo as odos, num as arit, tk
from m12_co
"""

from tedutil.fixed_size_file import ROW
from tedutil.fixed_size_file import COL
from tedutil.fixed_size_file import RowTyp
from tedutil.fixed_size_file import Row
from tedutil.fixed_size_file import Document
from tedutil.files import create_zip
from tedutil.grdate import today
from tedutil.sqlite import get_dict


def create_monthly_fmy(creation_date, year, data):
    co0 = [
        ('fnam', 8, COL.TXT),
        ('cdat', 8, COL.DAT),
        ('cycl', 4, COL.TXT),
        ('fil0', 127, COL.FIL)
    ]
    head = RowTyp(0, 'head', ROW.NOR, co0)
    co1 = [
        ('year', 4, COL.TXT),
        ('cepo', 18, COL.TXT),
        ('cono', 9, COL.TXT),
        ('cpat', 3, COL.TXT),
        ('eo', 1, COL.INT),  # επωνυμία (0) ή ονοματεώνυμο (1)
        ('cafm', 9, COL.INT),
        ('ant', 16, COL.TXT),  # αντικείμενο
        ('poli', 10, COL.TXT),
        ('odos', 16, COL.TXT),
        ('arit', 5, COL.TXT),
        ('tk', 5, COL.INT),
        ('month', 2, COL.INT),
        ('fil1', 49, COL.FIL)
    ]
    stoixeia = RowTyp(1, 'stoixeia', ROW.NOR, co1)
    co2 = [
        ('akapod', 16, COL.DEC),
        ('krat', 16, COL.DEC),
        ('kaapod', 16, COL.DEC),
        ('fi21', 15, COL.FI0),
        ('parfor', 15, COL.DEC),
        ('eea', 15, COL.DEC),
        ('xart', 14, COL.DEC),
        ('xoga', 13, COL.DEC),
        ('fi22', 27, COL.FIL)
    ]
    totals = RowTyp(2, 'totals', ROW.SUM, co2)
    co3 = [
        ('afm', 9, COL.TXT),
        ('fi31', 1, COL.FIL),
        ('epon', 18, COL.TXT),
        ('onom', 9, COL.TXT),
        ('patr', 3, COL.TXT),
        ('amka', 11, COL.TXT),
        ('paidia', 2, COL.INT),
        ('apty', 2, COL.INT),  # Τύπος αποδοχών
        ('akapod', 11, COL.DEC),
        ('krat', 10, COL.DEC),
        ('kaapod', 11, COL.DEC),
        ('allodapos', 1, COL.INT),
        ('xora', 2, COL.TXT),
        ('fsynt', 2, COL.INT),
        ('fi32', 5, COL.FI0),
        ('parfor', 10, COL.DEC),
        ('eea', 10, COL.DEC),
        ('xart', 9, COL.DEC),
        ('xoga', 8, COL.DEC),
        ('etanaf', 4, COL.INT),
        ('diat', 9, COL.TXT),
    ]
    details = RowTyp(3, 'details', ROW.NOR, co3)
    doc = Document()
    doc.add(Row(head, {'fnam': 'JL10', 'cdat': creation_date, 'cycl': year}))
    doc.add(Row(stoixeia, data['stoixeia']))
    doc.add(Row(totals))
    for line in data['details']:
        line['diat'] = '0000/0000'
        doc.add(Row(details, line))
    return doc.render()


def create_myf(etos, minas, trejimo=None):
    trejimo = trejimo or today()
    dat = {}
    fil = "/home/ted/Documents/myf-miniaia/mis.m13"
    sql1 = "SELECT * FROM codata"
    dat['stoixeia'] = get_dict(sql1, fil)[0]  # Only one line
    dat['stoixeia']['year'] = etos
    dat['stoixeia']['month'] = minas
    sql2 = "SELECT * FROM fmy where xrisi = '%s' and id=%s" % (etos, minas)
    dat['details'] = get_dict(sql2, fil)
    result = create_monthly_fmy(trejimo, etos, dat)
    tmina = '%s' % minas if minas >= 10 else '0%s' % minas
    outfile = '/home/ted/Downloads/akti%s%s.zip' % (etos, tmina)
    create_zip(result, outfile)


if __name__ == "__main__":
    create_myf(etos=2019, minas=2)
