from unittest import TestCase
from tedutil.file_fix_size import Row
from tedutil.file_fix_size import Document
from tedutil.file_fix_size import COLTYPE


class TestMake_file(TestCase):
    def test_make_file(self):
        r01 = Row(0, 'head', 0)
        r01.new_column('fnam', 8, COLTYPE.TXT)
        r01.new_column('dat', 8, COLTYPE.DAT)
        r01.new_column('cyc', 4, COLTYPE.TXT)
        r01.new_column('fil1', 148, COLTYPE.FIL)

        r02 = Row(1, "stoixeia", 0)
        r02.new_column('etos', 4, COLTYPE.TXT)
        r02.new_column('epon', 18, COLTYPE.TXT)
        r02.new_column('onom', 9, COLTYPE.TXT)
        r02.new_column('pat', 3, COLTYPE.TXT)

        r03 = Row(2, "detail", 0)
        r03.new_column('etos', 8, COLTYPE.TXT)
        r03.new_column('poso', 12, COLTYPE.DEC)
        r03.new_column('foro', 12, COLTYPE.DEC)

        r04 = Row(3, "test", 0)
        r04.new_column('vatt', 12, COLTYPE.DEC)

        doc = Document()
        doc.add_row_templates(r01, r02, r03, r04)
        # print(doc.row_templates["head"].size)
        # doc.adl({'n4m': 'head', 'fnam': 'JL10', 'dat': '20190403', 'cyc': '2019'})
        # doc.adl({'n4m': 'totals'})
        # doc.adl({'n4m': 'detail', 'poso': 100, 'foro': 0, 'nam': 'λΆΖΑΡΟς'})
        # doc.adl({'n4m': 'detail', 'poso': 123, 'foro': 12.2, 'nam': 'Μαυράκης'})
        # doc.adl({'n4m': 'test', 'vatt': 17.88, 'foro': 12.2, 'nam': 'Μαυράκης'})
        # doc.adl({'n4m': 'test', 'vatt': 17.88, 'foro': 12.2, 'nam': 'Μαυράκης'})
        # doc.adl({'n4m': 'test', 'vatt': 17.88, 'foro': 12.2, 'nam': 'Μαυράκης'})
        # print(r02)
        # print(doc.totals)
        # print(doc.render())
