from unittest import TestCase
from tedutil import grtext as grt


class TestGrup(TestCase):
    def test_grup_1(self):
        self.assertEqual('ΔΟΚΙΜΗ', grt.grup('δοκιμή'))

    def test_grup_2(self):
        self.assertEqual('15', grt.grup(15))

    def test_grup_3(self):
        self.assertEqual(grt.grup('tst1όέίάήώύ'), 'TST1ΟΕΙΑΗΩΥ')

    def test_split_strip(self):
        print(grt.split_strip('this|is|ted'))
