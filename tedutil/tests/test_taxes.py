from unittest import TestCase
from decimal import Decimal
from tedutil import taxes as tx1


class TestTaxes(TestCase):
    def test_foros_etoys(self):
        self.assertEqual(tx1.foros_etoys(2012, 110000), Decimal('36920'))

    def test_meiosi_foroy(self):
        self.assertEqual(tx1.meiosi_foroy(2019, 200000, 0), Decimal('100'))

    def test_foros_etoys_me_ekptosi(self):
        self.assertEqual(tx1.foros_etoys_me_ekptosi(2019, 14000),
                         Decimal('1180'))

    def test_eea_periodoy(self):
        self.assertEqual(tx1.eea_periodoy(2019, 1000, extra=100),
                         Decimal('5.34'))

    def test_foros_eea_periodoy(self):
        self.assertEqual(tx1.foros_eea_periodoy(2019, 1000, extra=100),
                         {'foros': Decimal('106.29'), 'eea': Decimal('5.34'),
                          'apodoxes': Decimal('1100.00'),
                          'pliroteo': Decimal('988.37')})
