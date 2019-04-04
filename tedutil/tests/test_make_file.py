from unittest import TestCase
from tedutil import file_fix_size as ffs


class TestMake_file(TestCase):
    def test_make_file(self):
        dat = {'l1': ['0', 'JL10', '20190328', '2019', ''],
               'l2': [1, 2019, 'ΝΙΚΟΠΟΛΙΣ ΑΕ', '', '', '', '094025817',
                      'ΔΙΑΦΟΡΑ', 'ΑΘΗΝΑ', 'φορμίονος', '13', '15235', '1', ''],
               'l3': [2, 30000, 7000, 23000, '', '', '', '', '', ''],
               'l4': [[3, '046949583', '', 'λαζαροσ', 'θεοδωρος', 'κωνσταντ',
                       '15026305175', 1, 1, 15000, 3500, 11500, 0, '', '', '',
                       0, 0, 0, 0, '', '', '/', ''],
                     [3, '012312312', '', 'Γεωργίου', 'Αλέκος', 'Αθανασιος',
                      '15026305175', 1, 1, 15000, 3500, 11500, 0, '', '', '',
                      0, 0, 0, 0, '', '', '/', ''],
                     ]}
        ffs.make_file(dat)
