from decimal import Decimal
from unittest import TestCase
from tedutil.fixed_size_file import LinePrototype, TextFile, fld

tx1 = """1ΛΑΖΑΡΟΣ                          00000000000000123454CSL01   15012020
2000000011534900000009000000010026000000024058
1ΜΑΥΡΑΚΗΣ                         00000000000000012300CSL01   18012020
EOF"""

di1 = [
    {
        'lineid': '1',
        'eponymo': 'ΛΑΖΑΡΟΣ',
        'fi1': ' ',
        'timi': Decimal('1234.54'),
        'st1': 'CSL01   ',
        'imnia': '2020-01-15'
    },
    {
        'lineid': '2',
        'apod': Decimal('115.34'),
        'afm': '900000009',
        'kre': Decimal('100.26'),
        'krt': Decimal('240.58')
    },
    {
        'lineid': '1',
        'eponymo': 'ΜΑΥΡΑΚΗΣ',
        'fi1': ' ',
        'timi': Decimal('123.00'),
        'st1': 'CSL01   ',
        'imnia': '2020-01-18'
    },
    {'lineid': 'EOF'}
]


class Test_Fixed_Size(TestCase):
    def test1(self):
        li1 = LinePrototype('1', 'Σύνολα')
        li1.add_field('eponymo', fld('txt_', siz=30), 'Επώνυμο')
        li1.add_field('fi1', fld('fill', siz=3, val=' '))
        li1.add_field('timi', fld('dec2', siz=20))
        li1.add_field('st1', fld('static', val='CSL01   '))
        li1.add_field('imnia', fld('dmy'))
        li2 = LinePrototype('2', 'Αναλυτικές γραμμές')
        li2.add_field('apod', fld('dec2', siz=12))
        li2.add_field('afm', fld('txt_', siz=9))
        li2.add_field('kre', fld('dec2', siz=12))
        li2.add_field('krt', fld('dec2', siz=12))
        eof = LinePrototype('EOF', 'Τέλος αρχείου')
        # eof.add_field('eof', StaticField('EOF'))
        csl = TextFile({'li1': li1, 'li2': li2, 'eof': eof})
        csl.add_line('li1', {'eponymo': 'Λάζαρος',
                             'timi': 1234.54, 'imnia': '2020-01-15'})
        csl.add_line('li2', {'apod': 115.34, 'afm': '900000009',
                             'kre': 100.26, 'krt': 240.58})
        csl.add_line('li1', {'eponymo': 'Μαυράκης',
                     'timi': '123', 'imnia': '2020-01-18'})
        csl.add_line('eof')
        txt1 = csl.text()
        self.assertEqual(txt1, tx1)
        self.assertEqual(di1, csl.revert(txt1))