from decimal import Decimal
from unittest import TestCase
from tedutil.fixed_size_file import DataLine, LinePrototype, TextFile, fld
from tedutil import fixed_size_file as fsf

tx1 = """1ΛΑΖΑΡΟΣ                          00000000000000123454CSL01   15012020
2000000011534900000009000000010026000000024058
1ΜΑΥΡΑΚΗΣ                         00000000000000012300CSL01   18012020
3CSL###00022001234       TEDPOPI      1001202020200111
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
    {
        'lineid': '3',
        'sta': 'CSL',
        'fil': '#',
        '0tx': '22',
        'de2': Decimal('12.34'),
        'ftx': 'TED',
        'btx': 'POPI',
        'dmy': '2020-01-10',
        'ymd': '2020-01-11'
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

        li3 = LinePrototype('3', 'Όλοι οι τύποι')
        li3.add_field('sta', fld('static', val='CSL'))
        li3.add_field('fil', fld('fill', siz=3, val='#'))
        li3.add_field('0tx', fld('0txt', siz=5))
        li3.add_field('de2', fld('dec2', siz=6))
        li3.add_field('ftx', fld('_txt', siz=10))
        li3.add_field('btx', fld('txt_', siz=10))
        li3.add_field('dmy', fld('dmy'))
        li3.add_field('ymd', fld('ymd'))

        eof = LinePrototype('EOF', 'Τέλος αρχείου')

        csl = TextFile({'li1': li1, 'li2': li2, 'li3': li3, 'eof': eof})

        csl.add_line('li1', {'eponymo': 'Λάζαρος',
                             'timi': 1234.54, 'imnia': '2020-01-15'})
        csl.add_line('li2', {'apod': 115.34, 'afm': '900000009',
                             'kre': 100.26, 'krt': 240.58})
        csl.add_line('li1', {'eponymo': 'Μαυράκης',
                     'timi': '123', 'imnia': '2020-01-18'})
        csl.add_line('li3', {'0tx': 22, 'de2': '12.34', 'ftx': 'ted',
                     'btx': 'popi', 'dmy': '2020-01-10', 'ymd': '2020-01-11'})
        csl.add_line('eof')
        txt1 = csl.text()
        self.assertEqual(txt1, tx1)
        self.assertEqual(di1, csl.revert(txt1))

    def test2(self):
        ztf1 = fsf.ZeroesTextField(2)
        self.assertRaises(ValueError, ztf1.text, 'ted')
        ztf2 = fsf.Decimal2Field(5)
        self.assertRaises(ValueError, ztf2.text, '1230.45')
        ztf3 = fsf.TextSpacesField(5)
        self.assertRaises(ValueError, ztf3.text, 'konstantinos')
        ztf4 = fsf.SpacesTextField(5)
        self.assertRaises(ValueError, ztf4.text, 'konstantinos')

    def test3(self):
        self.assertRaises(ValueError, fld, 'not_valid')
        li1 = LinePrototype('1', 'Σύνολα')
        li1.add_field('eponymo', fld('txt_', siz=30), 'Επώνυμο')
        self.assertRaises(ValueError, li1.add_field, 'eponymo', fld('ymd'))
        self.assertEqual(li1.number_of_fields, 1)
        msg = "Σύνολα με κωδικό 1 και πεδία ['eponymo'] συνολικού μεγέθους 31 χαρακτήρων"
        self.assertEqual(li1.__str__(), msg)
        dli = fsf.DataLine(li1)
        self.assertRaises(ValueError, dli.add_val, 'not_valid', 'teddy')
